from coke.parser import create_parser, ast

_PARSER = create_parser('alias')


def test_alias():
    assert _PARSER.parse('SomeType:') == ast.AliasNode(1, 0, 'SomeType')
