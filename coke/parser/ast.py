from typing import List, Any, Mapping, Union, Tuple, NamedTuple

ValueT = Union[
    'BooleanValueNode', 'NullValueNode', 'EnumValueNode', 'IntValueNode', 'FloatValueNode', 'EnumValueNode',
    'StringValueNode', 'ListValueNode',
]


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


class ListValueNode:
    __slots__ = 'line', 'column', 'items'

    def __init__(self, line: int, column: int, items: List[ValueT]):
        self.line = line
        self.column = column
        self.items = items

    def __eq__(self, other):
        return type(other) == type(self) and other.items == self.items

    def __repr__(self):
        return 'ListValue<{}:{} {!r}>'.format(self.line, self.column, self.items)


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


ObjectField = NamedTuple('ObjectField', [('name_node', NameNode), ('value_node', ValueT)])


class ObjectValueNode:
    __slots__ = 'line', 'column', 'field_nodes'

    def __init__(self, line: int, column: int, field_nodes: List[ObjectField]):
        self.line = line
        self.column = column
        self.field_nodes = field_nodes

    def __eq__(self, other):
        return type(other) == type(self) and other.field_nodes == self.field_nodes

    def __repr__(self):
        return 'ObjectValue<{}:{} {!r}>'.format(self.line, self.column, self.field_nodes)


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


class VariableNode:
    __slots__ = 'line', 'column', 'variable'

    def __init__(self, line: int, column: int, variable: str):
        self.line = line
        self.column = column
        self.variable = variable

    def __eq__(self, other):
        return type(other) == type(self) and other.variable == self.variable

    def __repr__(self):
        return 'Variable<{}:{} {}>'.format(self.line, self.column, self.variable)
