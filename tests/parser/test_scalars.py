from coke.parser import ast, create_parser


def test_parse_string_value():
    parser = create_parser('string_value')
    assert parser.parse('""') == ast.StringNode(1, 0, '')
    assert parser.parse('"foo"') == ast.StringNode(1, 0, 'foo')
    assert parser.parse('"\\u0066oo"') == ast.StringNode(1, 0, 'foo')
    assert parser.parse('"foo\\nbar"') == ast.StringNode(1, 0, 'foo\nbar')
    assert parser.parse('"a string # with a comment"') == ast.StringNode(1, 0, 'a string # with a comment')


def test_parse_int_value():
    parser = create_parser('int_value')
    assert parser.parse('-123') == ast.IntNode(1, 0, -123)
    assert parser.parse('-1') == ast.IntNode(1, 0, -1)
    assert parser.parse('-0') == ast.IntNode(1, 0, 0)
    assert parser.parse('0') == ast.IntNode(1, 0, 0)
    assert parser.parse('1') == ast.IntNode(1, 0, 1)
    assert parser.parse('123') == ast.IntNode(1, 0, 123)
    assert parser.parse('10000000') == ast.IntNode(1, 0, 10000000)


def test_parse_float_value():
    parser = create_parser('float_value')
    assert parser.parse('-123.456') == ast.FloatNode(1, 0, -123.456)
    assert parser.parse('42e3') == ast.FloatNode(1, 0, 42000.0)
    assert parser.parse('-0.12e3') == ast.FloatNode(1, 0, -0.12e3)


def test_parse_constant_value():
    parser = create_parser('constant_value')
    assert parser.parse('true') == ast.BooleanNode(1, 0, True)
    assert parser.parse('false') == ast.BooleanNode(1, 0, False)
    assert parser.parse('null') == ast.NullNode(1, 0, None)
    assert parser.parse('Null') == ast.EnumNode(1, 0, 'Null')


def test_parse_list_value():
    parser = create_parser('list_value')
    assert parser.parse('[1 2 3]') == ast.ListNode(1, 0, [
        ast.IntNode(1, 1, 1),
        ast.IntNode(1, 3, 2),
        ast.IntNode(1, 5, 3),
    ])
    assert parser.parse('[true false]') == ast.ListNode(1, 0, [
        ast.BooleanNode(1, 1, True),
        ast.BooleanNode(1, 6, False),
    ])
    assert parser.parse('["hello" "world!"]') == ast.ListNode(1, 0, [
        ast.StringNode(1, 1, 'hello'),
        ast.StringNode(1, 9, 'world!'),
    ])
    assert parser.parse(
        '[["hello", "world!"], [" "], ["nice " "to" " meet you"]]',
    ) == ast.ListNode(1, 0, [
        ast.ListNode(1, 1, [ast.StringNode(1, 2, 'hello'), ast.StringNode(1, 11, 'world!')]),
        ast.ListNode(1, 22, [ast.StringNode(1, 23, ' ')]),
        ast.ListNode(1, 29, [ast.StringNode(1, 30, 'nice '), ast.StringNode(1, 38, 'to'), ast.StringNode(1, 43, ' meet you')]),
    ])
    assert parser.parse('[]') == ast.ListNode(1, 0, [])


def test_parse_object_value():
    parser = create_parser('object_value')
    assert parser.parse('{hello: "world!"}') == ast.ObjectNode(1, 0, {ast.NameNode(1, 1, 'hello'): ast.StringNode(1, 8, 'world!')})
    assert parser.parse(
        '{hello: ["list" "of" "items"]}',
    ) == ast.ObjectNode(1, 0, {
        ast.NameNode(1, 1, 'hello'): ast.ListNode(1, 8, [
            ast.StringNode(1, 9, 'list'),
            ast.StringNode(1, 16, 'of'),
            ast.StringNode(1, 21, 'items'),
        ]),
    })


def test_parse_variable_value():
    parser = create_parser('variable')
    assert parser.parse('$myvar') == ast.VariableNode(1, 0, 'myvar')
