import pytest
from lark import UnexpectedInput

from coke.parser import create_parser, ast

_PARSER = create_parser('string_value')


def test_empty_string():
    """The empty string"""
    assert _PARSER.parse('""') == ast.StringValueNode(1, 0, '')


def test_single_char():
    """Parse a one char string"""
    assert _PARSER.parse('"x"') == ast.StringValueNode(1, 0, 'x')


def test_escaped_unicode_char():
    """0x78 is x in ascii/unicode"""
    assert _PARSER.parse('"\\u0078"') == ast.StringValueNode(1, 0, 'x')


def test_escaped_non_printable_unicode_char():
    """Unicode escape sequence for a non-printable character"""
    assert _PARSER.parse('"\\uffff"') == ast.StringValueNode(1, 0, '\uffff')


def test_unicode_bom_char():
    """Byte order mark chars are not allowed"""
    with pytest.raises(UnexpectedInput):
        _PARSER.parse('"\ufeff"')


def test_newline_char():
    """A newline character is allowed only in block strings"""
    with pytest.raises(UnexpectedInput):
        _PARSER.parse('"\n"')


def test_escaped_chars():
    assert _PARSER.parse('"\\n"') == ast.StringValueNode(1, 0, '\n')
    assert _PARSER.parse('"\\t"') == ast.StringValueNode(1, 0, '\t')
    assert _PARSER.parse('"\\r"') == ast.StringValueNode(1, 0, '\r')
    assert _PARSER.parse('"\\f"') == ast.StringValueNode(1, 0, '\f')
    assert _PARSER.parse('"\\""') == ast.StringValueNode(1, 0, '"')
    assert _PARSER.parse('"\\/"') == ast.StringValueNode(1, 0, '/')
