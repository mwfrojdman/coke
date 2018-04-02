from coke.parser import create_parser, ast

_PARSER = create_parser('enum_bool_or_null_value')


def test_null():
    assert _PARSER.parse('null') == ast.NullValueNode(1, 0)


def test_booleans():
    assert _PARSER.parse('true') == ast.BooleanValueNode(1, 0, True)
    assert _PARSER.parse('false') == ast.BooleanValueNode(1, 0, False)


def test_enums():
    # case sensitive -> not a boolean
    assert _PARSER.parse('True') == ast.EnumValueNode(1, 0, 'True')
    assert _PARSER.parse('NULL') == ast.EnumValueNode(1, 0, 'NULL')
    assert _PARSER.parse('ANOTHER_ENUM') == ast.EnumValueNode(1, 0, 'ANOTHER_ENUM')
