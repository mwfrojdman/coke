# -*- coding: utf-8 -*-
import logging

from lark import Lark, UnexpectedInput, Tree
import re

from lark.lexer import Token

log = logging.getLogger(__name__)


def test():
    assert 'f' == '\u0066'
    expected = Tree('start', [Token('ANONRE_0', 'f')])
    #fail: [\u0020-\u0021\u0023-\u005b\u005d-\ufefe\uff00-\uffff]
    assert Lark(r'''start: /[ !\#-\[\]-\ufefe\uff00-\uffff]/''').parse('f') == Tree('start', [Token('ANONRE_0', 'f')])
    # error in \u005b == '['
    assert Lark(r'''start: /[\u005d-\ufefe\uff00-\uffff]/''').parse('f') == expected
    assert Lark(r'''start: /[\u0061-\u0100\u0102-\u0200]/''').parse('f') == expected


def xyz():
    range_parts = [
        '\\u0020-\\u0021',
        '\\u0023-\\u005b',
        '\\u005d-\\ufefe',
        '\\uff00-\\uffff',
    ]
    char_range = '[{}]'.format(''.join(range_parts))
    assert char_range == r'[\u0020-\u0021\u0023-\u005b\u005d-\ufefe\uff00-\uffff]'
    assert re.match(r'^{}$'.format(char_range), 'f')

    assert Lark(r'start: /[\u0061-\u007a]/'.format(char_range)).parse('f')
    assert Lark(r'start: /[\u0061-\u0100]/'.format(char_range)).parse('f')
    assert Lark(r'start: /[\u0020-\u0021\u0023-\u005b\u005d-\ufefe\uff00-\uffff]/').parse('f')

    for i in range(2, len(range_parts) + 1):
        test_range = '[{}]'.format(''.join(range_parts[:i]))
        assert_parse(test_range)


def assert_parse(test_range):
    assert re.match(r'^{}$'.format(test_range), 'f')
    try:
        assert Lark(r'start: /{}/'.format(test_range)).parse('f')
    except UnexpectedInput:
        raise ValueError(test_range)
