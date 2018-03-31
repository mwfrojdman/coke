from coke.parser import create_parser

QUERY_ONE = """
query {
  fieldA
  fieldB (foo: 123)
  fieldC {
    subField
  }
}
""".strip()


def test_operation_definition():
    parser = create_parser('operation_definition')
    #assert parser.parse('query opname ($foo: Int bar: Str) { someField }') == ''
