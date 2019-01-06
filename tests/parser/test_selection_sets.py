from coke.parser import create_parser, ast

_PARSER = create_parser('fields')


def test_selection_set_with_single_field():
    assert _PARSER.parse('{fieldName}') == ast.SelectionSetNode(
        line=1,
        column=0,
        selection_nodes=[
            ast.FieldNode(
                line=1,
                column=1,
                alias_node=None,
                name_node=ast.NameNode(1, 1, 'fieldName'),
                arguments_node=None,
                directives_node=None,
                selection_set_node=None,
            ),
        ],
    )

def test_selection_set_with_two_fields():
    assert _PARSER.parse('fieldName anotherFieldName') == ast.SelectionSetNode(
        line=1,
        column=0,
        selection_nodes=[
            ast.FieldNode(
                line=1,
                column=1,
                alias_node=None,
                name_node=ast.NameNode(1, 1, 'fieldName'),
                arguments_node=None,
                directives_node=None,
                selection_set_node=None,
            ),
            ast.FieldNode(
                line=1,
                column=10,
                alias_node=None,
                name_node=ast.NameNode(1, 1, 'anotherFieldName'),
                arguments_node=None,
                directives_node=None,
                selection_set_node=None,
            ),
        ],
    )
