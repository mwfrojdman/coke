import json
import re
from typing import List, Iterable, Union

from lark import Lark, Transformer, inline_args
from lark.lexer import Token

from coke.parser.exceptions import ParseError
from . import ast

_GRAMMAR = r"""
_COLON: ":"
DBLQUOTE: "\""
DOLLAR: "$"
_BACKSLASH: "\\"
_EXCL: "!"
LBRACES: "{"
LBRACKET: "["
_RBRACES: "}"
_RBRACKET: "]"
LPAREN: "("
_RPAREN: ")"

TRIPLE_QUOTES: "\"\"\""
_UNICODE_ESCAPE: "\\u"
_ESCAPED_TRIPLE_QUOTES: "\\\"\"\""
ON_KEYWORD: "on"

alias: name _IGNORE? _COLON

argument: name _IGNORE? _COLON _IGNORE? value

arguments: LPAREN _IGNORE? argument (_IGNORE? argument)* _IGNORE? _RPAREN

?block_string_character: _ESCAPED_TRIPLE_QUOTES -> escaped_triple_double_quotes
    | /[\t\n\r -\ufefe\uff00-\uffff]/

enum_bool_or_null_value: name

float_value: /-?(0|[1-9][0-9]*)(\.[0-9]+([eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)/

int_value: /-?(0|[1-9][0-9]*)/

list_type: LBRACKET _IGNORE? type _IGNORE? _RBRACKET

list_value: LBRACKET _IGNORE? value* _IGNORE? _RBRACKET

name: /[_A-Za-z][_0-9A-Za-z]*/

named_type: name

non_null_type: (named_type | list_type) _IGNORE? _EXCL

object_field: name _IGNORE? _COLON _IGNORE? value

object_value: LBRACES object_field* _RBRACES

?string_character: /[ !\#-\[\]-\ufefe\uff00-\uffff]/ | string_character_escaped_unicode | string_character_escaped
string_character_escaped_unicode: _UNICODE_ESCAPE /[0-9A-Fa-f]{4}/
string_character_escaped: _BACKSLASH /[bfnrt"\\\/]/

string_value: DBLQUOTE string_character* DBLQUOTE -> quoted_string
    | TRIPLE_QUOTES block_string_character* TRIPLE_QUOTES -> block_string

?type: named_type
    | list_type
    | non_null_type

type_condition: ON_KEYWORD _IGNORE? named_type

?value: variable
    | int_value
    | float_value
    | string_value
    | enum_bool_or_null_value
    | list_value
    | object_value

variable: DOLLAR _IGNORE? name

_IGNORE: /([ \t\n\r,]+)|#[^\r\n]*/
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
    @inline_args
    def alias(self, name_node: ast.NameNode) -> ast.AliasNode:
        return ast.AliasNode(line=name_node.line, column=name_node.column, alias=name_node.name)

    @inline_args
    def argument(self, name_node: ast.NameNode, value_node: ast.ValueT) -> ast.Argument:
        return ast.Argument(name_node=name_node, value_node=value_node)

    def arguments(self, matches):
        lparen_token, *argument_nodes = matches
        return ast.ArgumentsNode(line=lparen_token.line, column=lparen_token.column, argument_nodes=argument_nodes)

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

    @inline_args
    def enum_bool_or_null_value(self, name_node: ast.NameNode):
        if name_node.name == 'null':
            return ast.NullValueNode(line=name_node.line, column=name_node.column)
        elif name_node.name == 'true':
            return ast.BooleanValueNode(line=name_node.line, column=name_node.column, value=True)
        elif name_node.name == 'false':
            return ast.BooleanValueNode(line=name_node.line, column=name_node.column, value=False)
        else:
            return ast.EnumValueNode(line=name_node.line, column=name_node.column, enum=name_node.name)

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
    def list_type(self, lbracket_token: Token, type_node: ast.TypeNodeT) -> ast.ListTypeNode:
        return ast.ListTypeNode(line=lbracket_token.line, column=lbracket_token.column, contained_type_node=type_node)

    @staticmethod
    def list_value(matches):
        lbracket_token, *item_nodes = matches
        return ast.ListValueNode(line=lbracket_token.line, column=lbracket_token.column, item_nodes=item_nodes)

    @inline_args
    def name(self, name_token: Token):
        return ast.NameNode(line=name_token.line, column=name_token.column, name=str(name_token))

    @inline_args
    def named_type(self, name_node: ast.NameNode) -> ast.NamedTypeNode:
        if name_node.name == 'null':
            raise ParseError(line=name_node.line, column=name_node.column, message='null is not an allowed named type')
        return ast.NamedTypeNode(line=name_node.line, column=name_node.column, type_name=name_node.name)

    @inline_args
    def non_null_type(self, type_node: ast.TypeNodeT) -> ast.NonNullTypeNode:
        return ast.NonNullTypeNode(line=type_node.line, column=type_node.column, nullable_type_node=type_node)

    @inline_args
    def object_field(self, name_node: ast.NameNode, value_node: ast.ValueT):
        return ast.ObjectField(name_node=name_node, value_node=value_node)

    @staticmethod
    def object_value(matches):
        lbraces_token, *field_nodes = matches
        return ast.ObjectValueNode(line=lbraces_token.line, column=lbraces_token.column, field_nodes=field_nodes)

    @inline_args
    def string_character_escaped(self, escaped_char: str) -> str:
        return _ESCAPED_CHARS[escaped_char]

    @inline_args
    def string_character_escaped_unicode(self, unicode_code_str: str) -> str:
        # unicode_code_str is four digits
        return chr(int(unicode_code_str, 16))

    @inline_args
    def type_condition(self, on_kw_token: Token, named_type_node: ast.NamedTypeNode) -> ast.TypeConditionNode:
        return ast.TypeConditionNode(
            line=on_kw_token.line,
            column=on_kw_token.column,
            type_name=named_type_node.type_name,
        )

    @staticmethod
    def quoted_string(matches: List[Union[str, Token]]) -> ast.StringValueNode:
        string_start, *matches, string_end = matches
        return ast.StringValueNode(line=string_start.line, column=string_start.column, string=''.join(matches))

    @inline_args
    def variable(self, dollar_token: Token, name_node: ast.NameNode) -> ast.VariableNode:
        assert dollar_token == '$'
        return ast.VariableNode(line=dollar_token.line, column=dollar_token.column, variable=name_node.name)


def create_parser(start: str) -> Lark:
    return Lark(_GRAMMAR, start=start, lexer='contextual', parser='lalr', transformer=_AstTransformer())
