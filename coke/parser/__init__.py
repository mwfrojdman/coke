import re
from collections import deque
from typing import List, Any, Union, NewType

from lark import Lark, inline_args, Transformer, Tree
from lark.lexer import Token

from coke.parser import ast

_GRAMMAR = r"""
document: definition+

definition: executable_definition // TODO? | type_system_definition

executable_definition: operation_definition | fragment_definition

operation_definition: operation_type name? variable_definitions? directives? selection_set
    | selection_set

operation_type: QUERY | MUTATION | SUBSCRIPTION
QUERY: "query"
MUTATION: "mutation"
SUBSCRIPTION: "subscription"


name: NAME
NAME: /[_A-Za-z][_0-9A-Za-z]*/

variable_definitions: LPAREN variable_definition+ RPAREN

variable_definition: variable ":" type default_value?

default_value: "=" value


?value: variable
    | int_value
    | float_value
    | string_value
    | constant_value
    | list_value
    | object_value

int_value: /-?(0|[1-9][0-9]*)/
float_value: /-?(0|[1-9][0-9]*)(\.[0-9]+([eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)/
string_value: DOUBLE_QUOTE string_character* DOUBLE_QUOTE -> simple_string
    | TRIPLE_QUOTES block_string_character* TRIPLE_QUOTES -> block_string
DOUBLE_QUOTE: "\""
TRIPLE_QUOTES: "\"\"\""
// \uFEFF = BOM, \u0022 = ", \u00FC = \ 
// XXX: this fails: /[\u0020-\u0021\u0023-\u005b\u005d-\ufefe\uff00-\uffff]/
?string_character: /[ !\#-\[\]-\ufefe\uff00-\uffff]/ -> src_char
    | "\\u" /[0-9A-Fa-f]{4}/ -> escaped_unicode
    | "\\" /[bfnrt"\\\/]/ -> escaped_character
?block_string_character: "\\\"\"\"" -> escaped_triple_double_quotes
    | /[\t\n\r -\ufefe\uff00-\uffff]/ -> block_char
constant_value: name
list_value: LIST_START value* "]"
LIST_START: "["
object_value: OPENING_BRACES object_field* "}"
OPENING_BRACES: "{"
?object_field: name ":" value

directives: directive+

directive: DIRECTIVE_START name arguments?
DIRECTIVE_START: "@"

arguments: LPAREN argument+ RPAREN
LPAREN: "("
RPAREN: ")"

argument: name ":" value

selection_set: OPENING_BRACES selection+ "}"  // XXX: + instead of *

//selection: field | fragment_spread | inline_fragment
selection: field | fragment_spread | inline_fragment

field: alias? name arguments? directives? selection_set?

alias: name ":"

type: named_type | list_type | non_null_type
named_type: name
list_type: "[" type "]"
non_null_type: (named_type | list_type) "!"

variable: VARIABLE_START name
VARIABLE_START: "$"

// "on" is not allowed in fragment name, but strings takes precedence over regular expression
fragment_definition: "fragment" name type_condition directives selection_set
type_condition: ON_KEYWORD named_type
ON_KEYWORD: "on"

fragment_spread: THREE_DOTS name directives?
THREE_DOTS: "..."

inline_fragment: THREE_DOTS type_condition? directives? selection_set

%ignore /([ \t\n\r,]+)|#[^\r\n]*/
"""


_ESCAPED_CHARS = {
    '"': '"',
    '\\': '\\',
    '/': '/',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
}


class TreeToDocument(Transformer):
    def simple_string(self, matches):
        string_start, *matches, string_end = matches
        chars = []
        for tree in matches:
            assert isinstance(tree, Tree), tree
            assert isinstance(tree.data, str), tree.data
            if tree.data == 'src_char':
                chars.extend(tree.children)
            elif tree.data == 'escaped_unicode':
                chars.extend(chr(int(''.join(tree.children), 16)))
            elif tree.data == 'escaped_character':
                escaped_char, = tree.children
                chars.append(_ESCAPED_CHARS[escaped_char])
            else:
                raise ValueError(tree.data)
        return ast.StringNode(string_start.line, string_start.column, ''.join(chars))

    @staticmethod
    def _block_string_lines(matches):
        """Generates unindented lines from block strings"""
        raw_lines = re.split(
            r'\r\n|\r|\n',  # XXX: \r\n has to come first
            ''.join(match.children[0] if match.data == 'block_char' else '"""' for match in matches),
        )

        common_indent = None

        for line in raw_lines[1:]:
            indent = 0
            for c in line:
                if c != ' ' and c != '\t':
                    break
                indent += 1
            else:
                continue
            if common_indent is None or indent < common_indent:
                common_indent = indent

        if common_indent is not None and common_indent > 0:
            yield raw_lines[0]
            for line in raw_lines[1:]:
                yield line[common_indent:]
        else:
            yield from raw_lines

    def block_string(self, matches):
        string_start, *matches, _ = matches

        lines = []
        lines_iter = self._block_string_lines(matches)

        # skips any blank or empty leading lines
        for line in lines_iter:
            if any(c != ' ' and c != '\t' for c in line):
                lines.append(line)
                break
        else:
            # nothing but empty/blank lines
            ast.StringNode(string_start.line, string_start.column, '')

        lines.extend(lines_iter)

        # remove trailing blank/empty lines
        for i, line in enumerate(reversed(lines)):
            if any(c != ' ' and c != '\t' for c in line):
                if i > 0:
                    del lines[-i:]
                break

        return ast.StringNode(string_start.line, string_start.column, '\n'.join(lines))

    @inline_args
    def int_value(self, match: Token):
        return ast.IntNode(match.line, match.column, int(match.value))

    @inline_args
    def float_value(self, match: Token):
        return ast.FloatNode(match.line, match.column, float(match.value))

    def name(self, args):
        name_token, = args
        return ast.NameNode(name_token.line, name_token.column, name_token.value)

    @inline_args
    def constant_value(self, name_node):
        """Handles boolean, null, and enums"""
        if not isinstance(name_node, ast.NameNode):
            raise TypeError(name_node)
        return name_node.constant_node()

    @inline_args
    def list_value(self, list_start_token, *item_nodes):
        # XXX: do list values have to be of the same type? ie. is mixing ints and strings allowed?
        return ast.ListNode(list_start_token.line, list_start_token.column, list(item_nodes))

    @inline_args
    def object_field(self, key, value):
        return key, value

    def object_value(self, matches):
        object_start, *matches = matches
        # TODO: check for duplicate keys
        return ast.ObjectNode(object_start.line, object_start.column, dict(matches))

    @inline_args
    def variable(self, variable_start, value: ast.NameNode):
        return ast.VariableNode(variable_start.line, variable_start.column, value.value)

    def variable_definition(self, *matches):
        return self._build_ast_node_from_matches(
            matches,
            [
                ('variable', ast.VariableNode, True, lambda v_node: v_node.value),
                ('type_node', (ast.NameNode, ast.ListTypeNode, ast.NonNullTypeNode), True),
                ('default_value', ast.ValueNode, False, OMITTED_DEFAULT_VALUE, None),
            ],
            ast.VariableDefinitionNode,
            new_style=True,
        )

    def variable_definitions(self, args):
        if args == []:
            return args
        raise ValueError(args)

    @inline_args
    def type(self, match):
        return match

    @inline_args
    def list_type(self, match):
        return ast.ListTypeNode(match)

    @inline_args
    def non_null_type(self, match):
        return ast.NonNullTypeNode(match)

    @inline_args
    def alias(self, name_node: ast.NameNode):
        return ast.AliasNode(name_node.line, name_node.column, name_node.value)

    def field(self, matches):
        # arguments? directives selection_set
        return self._build_ast_node_from_matches(
            matches,
            [
                ('alias', ast.AliasNode, False, None, None),
                ('name', ast.NameNode, True, None, None),
                ('arguments', ast.ArgumentsNode, False, {}, lambda a_node: a_node.value),
                ('directives', ast.DirectivesNode, False, [], lambda d_node: d_node.value),
                ('selection_set', ast.SelectionSet, False, [], lambda ss_node: ss_node.value),
            ],
            ast.FieldNode,
        )

    @staticmethod
    def _build_ast_node_from_matches(matches, fields, node_cls, *, ignore_tokens=(), new_style=False):
        i = 0
        kwargs = {}
        first_match = matches[0]
        matches = [match for match in matches if not isinstance(match, Token) or match.type not in ignore_tokens]
        for item in fields:
            if new_style:
                name, field_cls, required, *rest = item
                if not required:
                    default, *rest = rest
                if rest:
                    getter, = rest
                else:
                    getter = None
            else:
                name, field_cls, required, default, getter = item

            try:
                match = matches[i]
            except IndexError as exc:
                if required:
                    raise ValueError('Field {} is required. Was able to collect {!r}'.format(name, kwargs)) from exc
                else:
                    kwargs[name] = default
            else:
                if isinstance(match, field_cls):
                    if getter is None:
                        kwargs[name] = match
                    else:
                        kwargs[name] = getter(match)
                    i += 1
                elif required:
                    raise ValueError(name)
                else:
                    kwargs[name] = default
        if i != len(matches):
            raise ValueError('unused matches: {}'.format(matches[i:]))
        return node_cls(line=first_match.line, column=first_match.column, **kwargs)

    @inline_args
    def argument(self, name_node, value_node):
        return name_node, value_node

    def arguments(self, matches):
        arguments_start, *argument_nodes, _ = matches
        # TODO: check for duplicate argument names
        return ast.ArgumentsNode(arguments_start.line, arguments_start.column, dict(argument_nodes))

    def directives(self, matches):
        # TODO: check no overlapping directives?
        first_directive = matches[0]
        return ast.DirectivesNode(first_directive.line, first_directive.column, list(matches))

    def directive(self, matches):
        directive_start, name_node, *arguments_nodes = matches
        assert directive_start == '@'
        if arguments_nodes:
            arguments_node, = arguments_nodes
            arguments = dict(arguments_node.value)
        else:
            arguments = {}
        return ast.DirectiveNode(directive_start.line, directive_start.column, name_node, arguments)

    @inline_args
    def selection_set(self, selection_set_start, *selections):
        # TODO: check selections don't overlap
        return ast.SelectionSet(selection_set_start.line, selection_set_start.column, list(selections))

    @inline_args
    def selection(self, match):
        # selection: field | fragment_spread | inline_fragment
        return match

    def fragment_spread(self, matches):
        # fragment_spread: "..." fragment_name directives?
        return self._build_ast_node_from_matches(
            matches,
            [
                ('fragment_name', ast.NameNode, True, None, None),
                ('directives', ast.DirectivesNode, False, [], lambda d_node: d_node.value),
            ],
            ast.FragmentSpreadNode,
            ignore_tokens=('THREE_DOTS',),
        )

    def inline_fragment(self, matches):
        # inline_fragment: THREE_DOTS type_condition? directives selection_set
        return self._build_ast_node_from_matches(
            matches,
            [
                ('type_condition', ast.TypeConditionNode, False, None, lambda tc_node: tc_node.name),
                ('directives', ast.DirectivesNode, False, [], lambda d_node: d_node.value),
                ('selection_set', ast.SelectionSet, True, None, lambda ss_node: ss_node.value),
            ],
            ast.InlineFragmentNode,
            ignore_tokens=('THREE_DOTS',),
        )

    @inline_args
    def named_type(self, name_node):
        if name_node.value == 'null':
            raise ValueError('null is now an allowed named type')  # XXX: parse error
        return name_node  # XXX: need to create a named type node?

    @inline_args
    def type_condition(self, on_keyword, name_node):
        return ast.TypeConditionNode(line=on_keyword.line, column=on_keyword.column, name=name_node)

    def operation_definition(self, matches):
        return self._build_ast_node_from_matches(
            matches,
            [
                ('operation_type', ast.OperationTypeNode, True, None, lambda ot_node: ot_node.value),
                ('name_node', ast.NameNode, False, None, None),
                ('variable_definitions', ast.VariableDefinitionsNode, False, {}, lambda vd_node: vd_node.value),
                ('directives', ast.DirectivesNode, False, [], lambda d_node: d_node.value),
                ('selection_set', ast.SelectionSet, True, None, lambda ss_node: ss_node.value),
            ],
            ast.OperationDefinitionNode,
        )

    def operation_definitions(self, matches):
        raise ValueError(matches)

    @inline_args
    def operation_type(self, token):
        return ast.OperationTypeNode(token.line, token.column, token.value)


def create_parser(start):
    return Lark(_GRAMMAR, start=start, parser='lalr', lexer='contextual', transformer=TreeToDocument())


DOCUMENT_PARSER = create_parser('document')


class QueryDocument:
    pass


def parse_document(document_string: str) -> QueryDocument:
   pass
