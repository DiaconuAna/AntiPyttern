"""
This metric will measure internal versus external field accesses.
Intended as a placeholder for feature envy:
A Blob constantly accesses the fields of associated data classes.
"""
import ast
import inspect

class FieldAccesses(ast.NodeVisitor):
    def __init__(self, cls):
        self.cls = cls
        self.instance_fields = set()
        self.internal_access = {}
        self.external_access = {}

    def visit_Assign(self, node):
        """
        Counts how many asssigned fields are accessed.
        :param node:
        :return:
        """
        for target in node.targets:
            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                self.instance_fields.add(target.attr)
            self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.current_method = node.name
        self.internal_access[self.current_method] = 0
        self.external_access[self.current_method] = 0
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Case 1: self.x.y -> detecting external field access
        if (
                isinstance(node.value, ast.Attribute)
                and isinstance(node.value.value, ast.Name)
                and node.value.value.id == 'self'
        ):
            base = node.value.attr
            if base in self.instance_fields:
                self.external_access[self.current_method] += 1
            return
            # Do not count `self.base` here as internal

        # Case 2: self.x -> detecting internal field access (only if not part of a chain)
        elif isinstance(node.value, ast.Name) and node.value.id == 'self':
            if isinstance(node.ctx, ast.Load):  # accessing, not assigning
                if node.attr in self.instance_fields:
                    self.internal_access[self.current_method] += 1
                return

        self.generic_visit(node)

    def analyze(self):
        """Analyze the given class."""
        self.visit(self.cls)
        return self.internal_access, self.external_access
