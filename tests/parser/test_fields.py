from coke.parser import create_parser, ast

_PARSER = create_parser('field')


def test_field_with_name_only():
    assert _PARSER.parse('fieldName') == ast.FieldNode(
        line=1,
        column=0,
        alias_node=None,
        name_node=ast.NameNode(1, 0, 'fieldName'),
        arguments_node=None,
        directives_node=None,
        selection_set_node=None,
    )


def test_field_with_name_and_alias():
    assert _PARSER.parse('someAlias: fieldName') == ast.FieldNode(
        line=1,
        column=0,
        alias_node=ast.AliasNode(1, 0, 'someAlias'),
        name_node=ast.NameNode(1, 10, 'fieldName'),
        arguments_node=None,
        directives_node=None,
        selection_set_node=None,
    )


def test_field_with_name_and_arguments():
    assert _PARSER.parse('fieldName (arg1: null)') == ast.FieldNode(
        line=1,
        column=0,
        alias_node=None,
        name_node=ast.NameNode(1, 0, 'fieldName'),
        arguments_node=ast.ArgumentsNode(
            1, 10, [
                ast.Argument(ast.NameNode(1, 11, 'arg1'), ast.NullValueNode(1, 15)),
            ],
        ),
        directives_node=None,
        selection_set_node=None,
    )
