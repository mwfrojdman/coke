import json
import re
from typing import List, Iterable, Union

from lark import Lark, Transformer, inline_args
from lark.lexer import Token

from . import ast

_GRAMMAR = r"""
DBLQUOTE: "\""
_BACKSLASH: "\\"

TRIPLE_QUOTES: "\"\"\""
_UNICODE_ESCAPE: "\\u"
_ESCAPED_TRIPLE_QUOTES: "\\\"\"\""

?block_string_character: _ESCAPED_TRIPLE_QUOTES -> escaped_triple_double_quotes
    | /[\t\n\r -\ufefe\uff00-\uffff]/

float_value: /-?(0|[1-9][0-9]*)(\.[0-9]+([eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)/

int_value: /-?(0|[1-9][0-9]*)/

?string_character: /[ !\#-\[\]-\ufefe\uff00-\uffff]/ | string_character_escaped_unicode | string_character_escaped
string_character_escaped_unicode: _UNICODE_ESCAPE /[0-9A-Fa-f]{4}/
string_character_escaped: _BACKSLASH /[bfnrt"\\\/]/

string_value: DBLQUOTE string_character* DBLQUOTE -> quoted_string
    | TRIPLE_QUOTES block_string_character* TRIPLE_QUOTES -> block_string

"""


_ESCAPED_CHARS = {
    '"': '"',
    '\\': '\\',
    '/': '/',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
}


def _split_block_string_lines(string_parts: List[str]) -> Iterable[str]:
    # string_parts is a list of single character strings and triple quote strings
    """Generates unindented lines from block strings"""
    raw_lines = re.split(
        r'\r\n|\r|\n',  # NB: \r\n has to come first
        ''.join(string_parts),
    )

    common_indent = None

    for line in raw_lines[1:]:
        indent = 0
        for c in line:
            if c != ' ' and c != '\t':
                break
            indent += 1
        else:
            continue
        if common_indent is None or indent < common_indent:
            common_indent = indent

    if common_indent is not None and common_indent > 0:
        first_line, *remaining_lines = raw_lines
        yield first_line
        for line in remaining_lines:
            yield line[common_indent:]
    else:
        yield from raw_lines


class _AstTransformer(Transformer):
    @staticmethod
    def block_string(matches: List[Union[str, Token]]) -> ast.StringValueNode:
        string_start, *string_parts, _ = matches

        lines = []
        lines_iter = _split_block_string_lines(string_parts)

        # skips any blank or empty leading lines
        for line in lines_iter:
            if any(c != ' ' and c != '\t' for c in line):
                lines.append(line)
                break
        else:
            # nothing but empty/blank lines
            ast.StringValueNode(line=string_start.line, column=string_start.column, string='')

        lines.extend(lines_iter)

        # remove trailing blank/empty lines
        for i, line in enumerate(reversed(lines)):
            if any(c != ' ' and c != '\t' for c in line):
                if i > 0:
                    del lines[-i:]
                break

        return ast.StringValueNode(line=string_start.line, column=string_start.column, string='\n'.join(lines))

    @staticmethod
    def escaped_triple_double_quotes(escaped_triple_quotes: str) -> str:
        return '"""'

    @inline_args
    def float_value(self, float_token: Token):
        return ast.FloatValueNode(line=float_token.line, column=float_token.column, number=float(float_token))

    @inline_args
    def int_value(self, int_token: Token):
        return ast.IntValueNode(int_token.line, int_token.column, int(int_token))

    @inline_args
    def string_character_escaped(self, escaped_char: str) -> str:
        return _ESCAPED_CHARS[escaped_char]

    @inline_args
    def string_character_escaped_unicode(self, unicode_code_str: str) -> str:
        # unicode_code_str is four digits
        return chr(int(unicode_code_str, 16))

    @staticmethod
    def quoted_string(matches: List[Union[str, Token]]) -> ast.StringValueNode:
        string_start, *matches, string_end = matches
        return ast.StringValueNode(line=string_start.line, column=string_start.column, string=''.join(matches))


def create_parser(start: str) -> Lark:
    return Lark(_GRAMMAR, start=start, lexer='contextual', parser='lalr', transformer=_AstTransformer())
