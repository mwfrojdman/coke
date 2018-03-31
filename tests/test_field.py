from coke.parser import create_parser, ast

_FIELD_PARSER = create_parser('field')


def test_all():
    # field: alias? name arguments? directives selection_set?
    assert _FIELD_PARSER.parse('myAlias: someField (foo: 123, bar: "asdf") @myDirective') == ast.FieldNode(
        line=1,
        column=0,
        alias=ast.AliasNode(1, 0, 'myAlias'),
        name=ast.NameNode(1, 9, 'someField'),
        arguments={
            ast.NameNode(1, 20, 'foo'): ast.IntNode(1, 25, 123),
            ast.NameNode(1, 30, 'bar'): ast.StringNode(1, 35, 'asdf'),
        },
        directives=[
            ast.DirectiveNode(1, 43, ast.NameNode(1, 44, 'myDirective'), {}),
        ],
        selection_set=[],
    )


def test_no_alias():
    assert _FIELD_PARSER.parse('someField (arg: true)') == ast.FieldNode(
        line=1,
        column=0,
        alias=None,
        name=ast.NameNode(1, 0, 'someField'),
        arguments={
            ast.NameNode(1, 11, 'arg'): ast.BooleanNode(1, 16, True),
        },
        directives=[],
        selection_set=[],
    )


def test_name_only():
    assert _FIELD_PARSER.parse('someField') == ast.FieldNode(
        line=1,
        column=0,
        alias=None,
        name=ast.NameNode(1, 0, 'someField'),
        arguments={},
        directives=[],
        selection_set=[],
    )


def test_with_selection_set():
    assert _FIELD_PARSER.parse('nestedField { foo }') == ast.FieldNode(
        line=1,
        column=0,
        alias=None,
        name=ast.NameNode(1, 0, 'nestedField'),
        arguments={},
        directives=[],
        selection_set=[
            ast.FieldNode(
                line=1,
                column=14,
                alias=None,
                name=ast.NameNode(1, 14, 'foo'),
                arguments={},
                directives=[],
                selection_set=[],
            ),
        ],
    )


def test_with_fragment_spread():
    s = '''
nestedField {
  someField
  ...spreadField
}
'''.strip()
    assert _FIELD_PARSER.parse(s) == ast.FieldNode(
        line=1,
        column=0,
        alias=None,
        name=ast.NameNode(1, 0, 'nestedField'),
        arguments={},
        directives=[],
        selection_set=[
            ast.FieldNode(
                line=2,
                column=2,
                alias=None,
                name=ast.NameNode(2, 2, 'someField'),
                arguments={},
                directives=[],
                selection_set=[],
            ),
            ast.FragmentSpreadNode(
                line=3,
                column=2,
                fragment_name=ast.NameNode(3, 5, 'spreadField'),
                directives=[],
            )
        ],
    )


def test_inline_fragment():
    parser = create_parser('inline_fragment')
    assert parser.parse('''
... on SomeType @include(if: $someVar) {
  inlineField
}
'''.strip()) == ast.InlineFragmentNode(
        line=1,
        column=0,
        type_condition=ast.NameNode(1, 7, 'SomeType'),
        directives=[
            ast.DirectiveNode(
                line=1,
                column=16,
                name=ast.NameNode(1, 17, 'include', ),
                arguments={
                    ast.NameNode(1, 25, 'if'): ast.VariableNode(1, 29, 'someVar'),
                }
            )
        ],
        selection_set=[
            ast.FieldNode(
                line=2,
                column=2,
                alias=None,
                name=ast.NameNode(2, 2, 'inlineField'),
                arguments={},
                directives=[],
                selection_set=[],
            )
        ],
    )


def test_selection_with_inline_fragment():
    parser = create_parser('selection')
    assert parser.parse('... on SomeType {\n  inlineField\n}') == ast.InlineFragmentNode(
        line=1,
        column=0,
        type_condition=ast.NameNode(1, 7, 'SomeType'),
        directives=[],
        selection_set=[
            ast.FieldNode(
                line=2,
                column=2,
                alias=None,
                name=ast.NameNode(2, 2, 'inlineField'),
                arguments={},
                directives=[],
                selection_set=[],
            )
        ]
    )


def test_with_inline_fragment():
    s = '''
nestedField {
  someField
  ... on SomeType @include(if: $someVar) {
    inlineField
  }
}
'''.strip()
    assert repr(_FIELD_PARSER.parse(s)) == repr(ast.FieldNode(
        line=1,
        column=0,
        alias=None,
        name=ast.NameNode(1, 0, 'nestedField'),
        arguments={},
        directives=[],
        selection_set=[
            ast.FieldNode(
                line=2,
                column=2,
                alias=None,
                name=ast.NameNode(2, 2, 'someField'),
                arguments={},
                directives=[],
                selection_set=[],
            ),
            ast.InlineFragmentNode(
                line=3,
                column=2,
                type_condition=ast.NameNode(1, 9, 'SomeType'),
                directives=[
                    ast.DirectiveNode(
                        line=3,
                        column=18,
                        name=ast.NameNode(3, 19, 'include',),
                        arguments={
                            ast.NameNode(3, 27, 'if'): ast.VariableNode(3, 31, 'someVar'),
                        }
                    )
                ],
                selection_set=[
                    ast.FieldNode(
                        line=4,
                        column=4,
                        alias=None,
                        name=ast.NameNode(4, 4, 'inlineField'),
                        arguments={},
                        directives=[],
                        selection_set=[],
                    )
                ],
            )
        ],
    ))


def test_type_condition():
    parser = create_parser('type_condition')
    assert parser.parse('on SomeType') == ast.TypeConditionNode(1, 0, ast.NameNode(1, 3, 'SomeType'))
