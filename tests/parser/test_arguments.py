from coke.parser import create_parser, ast

_PARSER = create_parser('arguments')


def test_alias():
    assert _PARSER.parse('(foo: "123" bar : 123)') == ast.ArgumentsNode(
        line=1,
        column=0,
        argument_nodes=[
            ast.Argument(name_node=ast.NameNode(1, 1, 'foo'), value_node=ast.StringValueNode(1, 6, '123')),
            ast.Argument(name_node=ast.NameNode(1, 1, 'bar'), value_node=ast.IntValueNode(1, 6, 123)),
        ],
    )
