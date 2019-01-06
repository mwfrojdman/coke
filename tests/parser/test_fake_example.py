from lark import Lark, Transformer, inline_args

GRAMMAR = r"""
alias: name _IGNORE? ":"

name: /[_A-Za-z][_0-9A-Za-z]*/

field: (alias _IGNORE?)? name

fields: field (_IGNORE? field)*

_IGNORE: " "
"""


class DummyTransformer(Transformer):
    @inline_args
    def field(self, name, alias):
        return 'field(name={}, alias={})'.format(name, alias)

    def fields(self, matches):
        return matches


PARSER = Lark(GRAMMAR, start='fields', lexer='contextual', parser='lalr', transformer=DummyTransformer())


def test():
    assert PARSER.parse('hello world') == ['field(name=hello, alias=world)']
