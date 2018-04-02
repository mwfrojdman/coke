from coke.parser import create_parser, ast

_PARSER = create_parser('object_value')


def test_empty_object():
    assert _PARSER.parse('{}') == ast.ObjectValueNode(1, 0, [])


def test_object_of_ints():
    expected = ast.ObjectValueNode(
        line=1,
        column=0,
        field_nodes=[
            ast.ObjectField(ast.NameNode(1, 1, 'foo'), ast.IntValueNode(1, 2, 123)),
            ast.ObjectField(ast.NameNode(1, 8, 'bar'), ast.IntValueNode(1, 22, 456)),
        ],
    )
    assert _PARSER.parse('{foo:123bar:456}') == expected
