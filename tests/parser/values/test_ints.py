from coke.parser import create_parser, ast

_PARSER = create_parser('int_value')


def test_int():
    assert _PARSER.parse('123') == ast.IntValueNode(1, 0, 123)
