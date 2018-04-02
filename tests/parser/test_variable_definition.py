from coke.parser import create_parser, ast

_PARSER = create_parser('variable_definition')


def test_variable_definition():
    assert _PARSER.parse('$myVar: Int') == ast.VariableDefinitionNode


def test_many():
    parser = create_parser('variable_definitions')
    assert parser.parse('($myVar: Int)') == 'derp'
