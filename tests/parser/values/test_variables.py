from coke.parser import create_parser, ast

_PARSER = create_parser('variable')


def test_variable():
    assert _PARSER.parse('$myVar') == ast.VariableNode(1, 0, 'myVar')
