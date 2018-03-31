from typing import Any, Union, Optional, List


class BaseNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __eq__(self, other):
        raise NotImplementedError()


class AstNode(BaseNode):
    def __init__(self, line: int, column: int, value: Any):
        super().__init__(line, column)
        self.value = value

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                other.line == self.line and
                other.column == self.column and
                self.value == other.value
        )

    def __repr__(self):
        return '{} at line {}:{} with value {!r}'.format(self.__class__.__name__, self.line, self.column, self.value)


class BooleanNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class NullNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class EnumNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class NameNode(AstNode):
    __slots__ = 'line', 'column', 'value'

    def constant_node(self) -> Union[BooleanNode, NullNode, EnumNode]:
        if self.value == 'null':
            return NullNode(self.line, self.column, None)
        elif self.value == 'true':
            return BooleanNode(self.line, self.column, True)
        elif self.value == 'false':
            return BooleanNode(self.line, self.column, False)
        else:
            return EnumNode(self.line, self.column, self.value)

    def __hash__(self):
        return hash(self.value)


class AliasNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class IntNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class FloatNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class StringNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class ListNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class ObjectNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class VariableNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class DirectivesNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class DirectiveNode(BaseNode):
    __slots__ = 'line', 'column', 'name', 'arguments'

    def __init__(self, line: int, column: int, name: NameNode, arguments):
        super().__init__(line, column)
        self.name = name
        self.arguments = arguments

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                other.line == self.line and
                other.column == self.column and
                self.name == other.name and
                self.arguments == other.arguments
        )

    def __repr__(self):
        return (
            '{clsname} at line {line}:{col} with name {name}, and arguments {args}'
        ).format(
            clsname=self.__class__.__name__,
            line=self.line,
            col=self.column,
            name=self.name.value,
            args=self.arguments,
        )


class ArgumentsNode(AstNode):
    __slots__ = 'line', 'column', 'value'


class SelectionSet(AstNode):
    __slots__ = 'line', 'column', 'value'


class FieldNode(BaseNode):
    __slots__ = 'line', 'column', 'alias', 'name', 'arguments', 'directives', 'selection_set'

    def __init__(self, line: int, column: int, alias: Optional[AliasNode], name: NameNode, arguments, directives, selection_set):
        super().__init__(line, column)
        self.alias = alias
        self.name = name
        self.arguments = arguments
        self.directives = directives
        self.selection_set = selection_set

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                other.line == self.line and
                other.column == self.column and
                self.alias == other.alias and
                self.name == other.name and
                self.arguments == other.arguments and
                self.directives == other.directives and
                self.selection_set == other.selection_set
        )

    def __repr__(self):
        return (
            '{clsname} at line {line}:{col} with name {name}, alias {alias}, arguments {args}, directives {dirs}, and selection set {selection_set}'
        ).format(
            clsname=self.__class__.__name__,
            line=self.line,
            col=self.column,
            name=self.name.value,
            alias=None if self.alias is None else self.alias.value,
            args=self.arguments,
            dirs=self.directives,
            selection_set=self.selection_set,
        )


class FragmentSpreadNode(BaseNode):
    __slots__ = 'line', 'column', 'fragment_name', 'directives'

    def __init__(self, line: int, column: int, fragment_name: NameNode, directives):
        super().__init__(line, column)
        self.fragment_name = fragment_name
        self.directives = directives

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                other.line == self.line and
                other.column == self.column and
                self.fragment_name == other.fragment_name and
                self.directives == other.directives
        )

    def __repr__(self):
        return (
            '{clsname} at line {line}:{col} with name {name}, and directives {dirs}'
        ).format(
            clsname=self.__class__.__name__,
            line=self.line,
            col=self.column,
            name=self.fragment_name.value,
            dirs=self.directives,
        )


class InlineFragmentNode(BaseNode):
    __slots__ = 'line', 'column', 'type_condition', 'directives', 'selection_set'

    def __init__(self, line: int, column: int, type_condition: Optional[Any], directives: List[Any], selection_set: List[Any]):
        super().__init__(line, column)
        self.type_condition = type_condition
        self.directives = directives
        self.selection_set = selection_set

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                other.line == self.line and
                other.column == self.column and
                self.type_condition == other.type_condition and
                self.directives == other.directives and
                self.selection_set == other.selection_set
        )

    def __repr__(self):
        return (
            '{clsname} at line {line}:{col} with type condition {type_cond}, directives {dirs}, and selection set '
            '{selection_set}'
        ).format(
            clsname=self.__class__.__name__,
            line=self.line,
            col=self.column,
            type_cond=self.type_condition.value,
            dirs=self.directives,
            selection_set=self.selection_set,
        )


class TypeConditionNode(BaseNode):
    __slots__ = 'line', 'column', 'name'

    def __init__(self, line: int, column: int, name: NameNode):
        super().__init__(line, column)
        self.name = name

    def __eq__(self, other):
        return (
                type(other) == type(self) and
                other.line == self.line and
                other.column == self.column and
                self.name == other.name
        )

    def __repr__(self):
        return '{clsname} at line {line}:{col} with type name {name}'.format(
            clsname=self.__class__.__name__,
            line=self.line,
            col=self.column,
            name=self.name.value,
        )
