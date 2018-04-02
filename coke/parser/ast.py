class StringValueNode:
    __slots__ = 'line', 'column', 'string'

    def __init__(self, line: int, column: int, string: str):
        self.line = line
        self.column = column
        self.string = string

    def __eq__(self, other):
        return type(other) == type(self) and other.value == self.string

    def __repr__(self):
        return 'StringValue<{}:{} {!r}>'.format(self.line, self.column, self.string)
