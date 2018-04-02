from typing import List, Any, Mapping, Union, Tuple, NamedTuple

ValueT = Union[
    'BooleanValueNode', 'NullValueNode', 'EnumValueNode', 'IntValueNode', 'FloatValueNode', 'EnumValueNode',
    'StringValueNode', 'ListValueNode',
]

TypeNodeT = Union['NamedTypeNode', 'ListTypeNode', 'NonNullTypeNode']


class AliasNode:
    __slots__ = 'line', 'column', 'alias'

    def __init__(self, line: int, column: int, alias: str):
        self.line = line
        self.column = column
        self.alias = alias

    def __eq__(self, other):
        return type(other) == type(self) and other.alias == self.alias

    def __repr__(self):
        return 'Alias<{}:{} {}>'.format(self.line, self.column, self.alias)


Argument = NamedTuple('Argument', [('name_node', 'NameNode'), ('value_node', ValueT)])


class ArgumentsNode:
    __slots__ = 'line', 'column', 'argument_nodes'

    def __init__(self, line: int, column: int, argument_nodes: List[Argument]):
        self.line = line
        self.column = column
        self.argument_nodes = argument_nodes

    def __eq__(self, other):
        return type(other) == type(self) and other.argument_nodes == self.argument_nodes

    def __repr__(self):
        return 'Arguments<{}:{} {!r}>'.format(self.line, self.column, self.argument_nodes)


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


class ListTypeNode:
    __slots__ = 'line', 'column', 'contained_type_node'

    def __init__(self, line: int, column: int, contained_type_node: TypeNodeT):
        self.line = line
        self.column = column
        self.contained_type_node = contained_type_node

    def __eq__(self, other):
        return type(other) == type(self) and other.contained_type_node == self.contained_type_node

    def __repr__(self):
        return 'ListType<{}:{} {!r}>'.format(self.line, self.column, self.contained_type_node)


class ListValueNode:
    __slots__ = 'line', 'column', 'item_nodes'

    def __init__(self, line: int, column: int, item_nodes: List[ValueT]):
        self.line = line
        self.column = column
        self.item_nodes = item_nodes

    def __eq__(self, other):
        return type(other) == type(self) and other.item_nodes == self.item_nodes

    def __repr__(self):
        return 'ListValue<{}:{} {!r}>'.format(self.line, self.column, self.item_nodes)


class NamedTypeNode:
    __slots__ = 'line', 'column', 'type_name'

    def __init__(self, line: int, column: int, type_name: str):
        self.line = line
        self.column = column
        self.type_name = type_name

    def __eq__(self, other):
        return type(other) == type(self) and other.type_name == self.type_name

    def __repr__(self):
        return 'NamedType<{}:{} {}>'.format(self.line, self.column, self.type_name)


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


class NonNullTypeNode:
    __slots__ = 'line', 'column', 'nullable_type_node'

    def __init__(self, line: int, column: int, nullable_type_node: TypeNodeT):
        self.line = line
        self.column = column
        self.nullable_type_node = nullable_type_node

    def __eq__(self, other):
        return type(other) == type(self) and other.nullable_type_node == self.nullable_type_node

    def __repr__(self):
        return 'NonNullType<{}:{} {!r}>'.format(self.line, self.column, self.nullable_type_node)


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


class TypeConditionNode:
    __slots__ = 'line', 'column', 'type_name'

    def __init__(self, line: int, column: int, type_name: str):
        self.line = line
        self.column = column
        self.type_name = type_name

    def __eq__(self, other):
        return type(other) == type(self) and other.type_name == self.type_name

    def __repr__(self):
        return 'TypeCondition<{}:{} {!r}>'.format(self.line, self.column, self.type_name)


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
