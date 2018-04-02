from coke.parser import create_parser, ast

_PARSER = create_parser('list_value')


def test_empty_list():
    assert _PARSER.parse('[]') == ast.ListValueNode(1, 0, [])


def test_list_of_strings():
    expected = ast.ListValueNode(
        line=1,
        column=0,
        item_nodes=[
            ast.StringValueNode(1, 1, 'hello'),
            ast.StringValueNode(1, 8, 'world')
        ]
    )
    assert _PARSER.parse('["hello""world"]') == expected
