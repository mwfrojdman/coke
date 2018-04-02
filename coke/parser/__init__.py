from lark import Lark, Transformer, inline_args

from . import ast

_GRAMMAR = r"""
DBLQUOTE: "\""
_BACKSLASH: "\\"

?string_character: STRING_CHARACTER_UNESCAPED | string_character_escaped_unicode | string_character_escaped
STRING_CHARACTER_UNESCAPED: /[ !\#-\[\]-\ufefe\uff00-\uffff]/
string_character_escaped_unicode: _UNICODE_ESCAPE /[0-9A-Fa-f]{4}/
_UNICODE_ESCAPE: "\\u"
string_character_escaped: _BACKSLASH /[bfnrt"\\\/]/

string_value: DBLQUOTE string_character* DBLQUOTE -> string_value
"""


def create_parser(start: str) -> Lark:
    return Lark(_GRAMMAR, start=start, lexer='contextual', parser='lalr', transformer=_AstTransformer())


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


class _AstTransformer(Transformer):
    @inline_args
    def string_character_escaped(self, escaped_char):
        return _ESCAPED_CHARS[escaped_char]

    @inline_args
    def string_character_escaped_unicode(self, unicode_code_str):
        # unicode_code_str is four digits
        return chr(int(unicode_code_str, 16))

    @staticmethod
    def string_value(matches):
        string_start, *matches, string_end = matches
        return ast.StringValueNode(line=string_start.line, column=string_start.column, value=''.join(matches))
