import pytest

from coke.parser import create_parser, ast, ParseError

_TYPE_PARSER = create_parser('type')
_NAMED_TYPE_PARSER = create_parser('named_type')
_LIST_TYPE_PARSER = create_parser('list_type')
_NON_NULL_TYPE_PARSER = create_parser('non_null_type')


def test_named_type():
    for parser in _TYPE_PARSER, _NAMED_TYPE_PARSER:
        assert parser.parse('SomeType') == ast.NamedTypeNode(1, 0, 'SomeType')


def test_null_as_named_type():
    for parser in _TYPE_PARSER, _NAMED_TYPE_PARSER:
        with pytest.raises(ParseError) as excinfo:
            parser.parse('null')
        assert excinfo.value.message == 'null is not an allowed named type'


def test_list_type():
    for parser in _TYPE_PARSER, _LIST_TYPE_PARSER:
        assert parser.parse('[SomeType]') == ast.ListTypeNode(1, 0, ast.NamedTypeNode(1, 1, 'SomeType'))
        assert parser.parse('[SomeType!]') == ast.ListTypeNode(
            1, 0, ast.NonNullTypeNode(1, 0, ast.NamedTypeNode(1, 1, 'SomeType')),
        )


def test_non_null_type():
    """Also tests combinations of non null and list"""
    for parser in _TYPE_PARSER, _NON_NULL_TYPE_PARSER:
        assert parser.parse('SomeType!') == ast.NonNullTypeNode(1, 0, ast.NamedTypeNode(1, 1, 'SomeType'))
        assert parser.parse('[SomeType]!') == ast.NonNullTypeNode(
            1, 0, ast.ListTypeNode(1, 1, ast.NamedTypeNode(1, 1, 'SomeType')),
        )
        assert parser.parse('[SomeType!]!') == ast.NonNullTypeNode(
            1, 0, ast.ListTypeNode(1, 1, ast.NonNullTypeNode(1, 1, ast.NamedTypeNode(1, 1, 'SomeType'))),
        )
