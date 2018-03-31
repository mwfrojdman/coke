from coke.parser import create_parser, ast


def test_parse_directive():
    parser = create_parser('directive')

    assert parser.parse('@myDirective') == ast.DirectiveNode(1, 0, ast.NameNode(1, 1, 'myDirective'), {})


def test_parse_directive_with_args():
    parser = create_parser('directive')

    assert parser.parse('@myDirective (foo: 123 bar: "asdf")') == ast.DirectiveNode(
        1, 0,
        ast.NameNode(1, 1, 'myDirective'),
        {
            ast.NameNode(1, 14, 'foo'): ast.IntNode(1, 19, 123),
            ast.NameNode(1, 23, 'bar'): ast.StringNode(1, 28, 'asdf'),
        },
    )
