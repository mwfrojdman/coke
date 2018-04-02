from coke.parser import create_parser, ast

_PARSER = create_parser('directives')


def test_directive_without_args():
    assert _PARSER.parse('@ MyDirective') == ast.DirectivesNode(
        line=1,
        column=0,
        directive_nodes=[
            ast.DirectiveNode(line=1, column=0, name_node=ast.NameNode(1, 1, 'MyDirective'), arguments_node=None),
        ],
    )
