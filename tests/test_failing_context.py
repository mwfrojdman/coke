from lark import Lark

GRAMMAR = r"""
selection: fragment_spread | inline_fragment

fragment_spread: THREE_DOTS fragment_name
THREE_DOTS: "..."

name: NAME
NAME: /[_A-Za-z][_0-9A-Za-z]*/
// same as name but excluding "on"
fragment_name: /([_A-Za-np-z][_0-9A-Za-z]*)|(o([_0-9A-Za-mo-z][_0-9A-Za-z]*|n[_0-9A-Za-z]+)?)/

inline_fragment: THREE_DOTS type_condition?
type_condition: ON_KEYWORD named_type
ON_KEYWORD: "on"
named_type: name

%ignore /([ \t\n\r,]+)|#[^\r\n]*/
"""

PARSER = Lark(GRAMMAR, start='selection', parser='lalr', lexer='contextual')


def test():
    assert PARSER.parse('... on SomeType') == ''



OTHER_GRAMMAR = r"""
fragment: "..." name (fragment_spread | inline_fragment)

fragment_spread: directives?
inline_fragment: 

fragment: "..." name (fragment_spread | inline_fragment)

fragment_spread: fragment_name

inline_fragment: type_condition?
type_condition: "on" name

name: NAME
NAME: /[_A-Za-z][_0-9A-Za-z]*/
// same as name but excluding "on"
fragment_name: /([_A-Za-np-z][_0-9A-Za-z]*)|(o([_0-9A-Za-mo-z][_0-9A-Za-z]*|n[_0-9A-Za-z]+)?)/

%ignore /([ \t\n\r,]+)|#[^\r\n]*/
"""

OTHER_PARSER = Lark(OTHER_GRAMMAR, start='selection', parser='lalr', lexer='contextual')
