class FloatValueNode:
    __slots__ = 'line', 'column', 'number'

    def __init__(self, line: int, column: int, number: float):
        self.line = line
        self.column = column
        self.number = number

    def __eq__(self, other):
        return type(other) == type(self) and other.number == self.number

    def __repr__(self):
        return 'FloatValue<{}:{} {}>'.format(self.line, self.column, self.number)


class IntValueNode:
    __slots__ = 'line', 'column', 'integer'

    def __init__(self, line: int, column: int, integer: int):
        self.line = line
        self.column = column
        self.integer = integer

    def __eq__(self, other):
        return type(other) == type(self) and other.integer == self.integer

    def __repr__(self):
        return 'IntValue<{}:{} {}>'.format(self.line, self.column, self.integer)


class StringValueNode:
    __slots__ = 'line', 'column', 'string'

    def __init__(self, line: int, column: int, string: str):
        self.line = line
        self.column = column
        self.string = string

    def __eq__(self, other):
        return type(other) == type(self) and other.string == self.string

    def __repr__(self):
        return 'StringValue<{}:{} {!r}>'.format(self.line, self.column, self.string)
