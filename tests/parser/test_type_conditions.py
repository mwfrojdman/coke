from coke.parser import create_parser, ast, ParseError


_PARSER = create_parser('type_condition')


def test_type_condition():
    assert _PARSER.parse('on SomeType') == ast.TypeConditionNode(1, 0, 'SomeType')
