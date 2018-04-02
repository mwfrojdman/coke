from typing import List

from coke.parser import create_parser, ast

_PARSER = create_parser('string_value')


def _assert_eq_from_lines(block_lines: List[str], expected_lines: List[str]):
    block_string = '"""{}"""'.format('\n'.join(block_lines))
    expected_string = '\n'.join(expected_lines)
    assert _PARSER.parse(block_string) == ast.StringValueNode(1, 0, expected_string)


def test_escaped_triple_quote():
    assert _PARSER.parse('"""x\\"""y"""') == ast.StringValueNode(1, 0, 'x"""y')


def test_uniform_indentation():
    """Remove indentation from block string"""
    block_lines = [
        '',
        '    Hello,',
        '      World!',
        '',
        '    Yours,',
        '      GraphQL.',
    ]
    expected_lines = [
        'Hello,',
        '  World!',
        '',
        'Yours,',
        '  GraphQL.',
    ]
    _assert_eq_from_lines(block_lines, expected_lines)


def test_strip_empty_lines():
    """Remove empty leading and trailing lines"""
    block_lines = [
        '',
        '',
        '    Hello,',
        '      World!',
        '',
        '    Yours,',
        '      GraphQL.',
        '',
        '',
    ]
    expected_lines = [
        'Hello,',
        '  World!',
        '',
        'Yours,',
        '  GraphQL.',
    ]
    _assert_eq_from_lines(block_lines, expected_lines)


def test_strip_blank_lines():
    """Removes blank leading and trailing lines"""
    block_lines = [
        '  ',
        '        ',
        '    Hello,',
        '      World!',
        '',
        '    Yours,',
        '      GraphQL.',
        '        ',
        '  ',
    ]
    expected_lines = [
        'Hello,',
        '  World!',
        '',
        'Yours,',
        '  GraphQL.',
    ]
    _assert_eq_from_lines(block_lines, expected_lines)


def test_retain_first_line_indent():
    block_lines = [
        '    Hello,',
        '      World!',
        '',
        '    Yours,',
        '      GraphQL.',
    ]
    expected_lines = [
        '    Hello,',
        '  World!',
        '',
        'Yours,',
        '  GraphQL.',
    ]
    _assert_eq_from_lines(block_lines, expected_lines)


def test_retain_trailing_spaces():
    block_lines = [
        '               ',
        '    Hello,     ',
        '      World!   ',
        '               ',
        '    Yours,     ',
        '      GraphQL. ',
        '               ',
    ]
    expected_lines = [
        'Hello,     ',
        '  World!   ',
        '           ',
        'Yours,     ',
        '  GraphQL. ',
    ]
    _assert_eq_from_lines(block_lines, expected_lines)


def test_empty():
    assert _PARSER.parse('""""""') == ast.StringValueNode(1, 0, '')


def test_only_empty_lines():
    assert _PARSER.parse('"""\n\n\n"""') == ast.StringValueNode(1, 0, '')


def test_only_blank_lines():
    assert _PARSER.parse('"""   \n  \n\t\t\n"""') == ast.StringValueNode(1, 0, '')


def test_two_lines():
    assert _PARSER.parse('"""hello\nworld"""') == ast.StringValueNode(1, 0, 'hello\nworld')


def test_escaped_triple_quotes():
    assert _PARSER.parse('"""hello\\"""world"""') == ast.StringValueNode(1, 0, 'hello"""world')


def test_escaped_double_quotes():
    """backslash + two double quotes should not be escaped"""
    assert _PARSER.parse('"""hello\\""world"""') == ast.StringValueNode(1, 0, 'hello\\""world')


def test_escaped_quotes():
    """backslash + double quotes should not be escaped"""
    assert _PARSER.parse('"""hello\\"world"""') == ast.StringValueNode(1, 0, 'hello\\"world')


def test_escaped_n():
    """backslash + n should not be interpreted as an escaped newline character"""
    assert _PARSER.parse('"""hello\\nworld"""') == ast.StringValueNode(1, 0, 'hello\\nworld')
