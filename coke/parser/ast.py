class BooleanValueNode:
    __slots__ = 'line', 'column', 'value'

    def __init__(self, line: int, column: int, value: bool):
        self.line = line
        self.column = column
        self.value = value

    def __eq__(self, other):
        return type(other) == type(self) and other.value is self.value

    def __repr__(self):
        return 'BooleanValue<{}:{} {}>'.format(self.line, self.column, self.value)


class EnumValueNode:
    __slots__ = 'line', 'column', 'enum'

    def __init__(self, line: int, column: int, enum: str):
        # enum must not be "null", "true", or "false"
        self.line = line
        self.column = column
        self.enum = enum

    def __eq__(self, other):
        return type(other) == type(self) and other.enum == self.enum

    def __repr__(self):
        return 'EnumValue<{}:{} {}>'.format(self.line, self.column, self.enum)


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


class NameNode:
    __slots__ = 'line', 'column', 'name'

    def __init__(self, line: int, column: int, name: str):
        self.line = line
        self.column = column
        self.name = name

    def __eq__(self, other):
        return type(other) == type(self) and other.name == self.name

    def __repr__(self):
        return 'Name<{}:{} {}>'.format(self.line, self.column, self.name)


class NullValueNode:
    __slots__ = 'line', 'column'

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __eq__(self, other):
        return type(other) == type(self)

    def __repr__(self):
        return 'NullValue<{}:{}>'.format(self.line, self.column)


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
