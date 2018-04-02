from coke.parser import create_parser, ast

_PARSER = create_parser('operation_definition')


def test_with_name():
    # XXX: no vars
    # XXX: no directives
    s = 'query myOperation { someField }'
    assert _PARSER.parse(s) == ast.OperationDefinitionNode(
        line=1,
        column=0,
        operation_type='query',
        name_node=ast.NameNode(line=1, column=6, value='myOperation'),
        variable_definitions={},
        directives=[],
        selection_set=[
            ast.FieldNode(
                line=1,
                column=20,
                alias=None,
                name=ast.NameNode(1, 20, 'someField'),
                arguments={},
                directives=[],
                selection_set=[],
            ),
        ],
    )
