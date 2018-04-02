import json

import pytest
from lark import UnexpectedInput

from coke.parser import create_parser, ast

_PARSER = create_parser('float_value')


def test_integer_is_not_valid_float():
    with pytest.raises(UnexpectedInput):
        _PARSER.parse('123')


def test_fractional():
    assert _PARSER.parse('123.456') == ast.FloatValueNode(1, 0, 123.456)
    assert _PARSER.parse('-123.456') == ast.FloatValueNode(1, 0, -123.456)
    assert _PARSER.parse('-0.123') == ast.FloatValueNode(1, 0, -0.123)
    assert _PARSER.parse('0.0') == ast.FloatValueNode(1, 0, 0.0)
    assert _PARSER.parse('-0.0') == ast.FloatValueNode(1, 0, 0.0)


def test_exponent():
    assert _PARSER.parse('123e0') == ast.FloatValueNode(1, 0, 123.0)
    assert _PARSER.parse('123e10') == ast.FloatValueNode(1, 0, 123e10)
    assert _PARSER.parse('-123e10') == ast.FloatValueNode(1, 0, -123e10)
    assert _PARSER.parse('123e+10') == ast.FloatValueNode(1, 0, 123e10)
    # no negative exponents in python float literals
    assert _PARSER.parse('123e-10') == ast.FloatValueNode(1, 0, float('123e-10'))
    assert _PARSER.parse('-123e-1') == ast.FloatValueNode(1, 0, float('-123e-1'))
