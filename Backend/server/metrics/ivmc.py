import ast
import sys
from collections import defaultdict

from metrics.number_of_methods import compute_nom_for_class

"""
IVMC - Metric introduced by James Munro
- number of methods that reference each instance variable defined in a class
"""

class IVMCAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.class_field_usage = dict()
        self.current_class = None
        self.current_method = None
        self.field_usage = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.field_usage = defaultdict(set)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.current_method = item.name
                self.generic_visit(item)

        self.class_field_usage[self.current_class] = {field: methods for field, methods in self.field_usage.items()}
        self.current_method = None
        self.field_usage = None
        self.current_class = None

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'self' and self.current_method:
            self.field_usage[node.attr].add(self.current_method)
        self.generic_visit(node)


def compute_ivmc_from_file(filename):
    with open(filename, "r") as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    analyzer = IVMCAnalyzer()
    analyzer.visit(tree)
    class_ivmc = dict()
    for class_name, field_methods in analyzer.class_field_usage.items():
        class_ivmc[class_name] = {field: len(methods) for field, methods in field_methods.items()}

    return class_ivmc


def compute_ivmc_per_class(source_code: str, target_class: str) -> dict[str, int] | None:
    tree = ast.parse(source_code)
    analyzer = IVMCAnalyzer()
    analyzer.visit(tree)

    field_methods = analyzer.class_field_usage.get(target_class)
    if field_methods is None:
        return None

    return {field: len(methods) for field, methods in field_methods.items()}


def compute_field_usage_percentage_per_class(source_code, target_class):
    """
    usage_ratio = (methods_using_field / total_methods) * 100

    :param source_code:
    :param target_class:
    :return:
    """
    class_nom = compute_nom_for_class(source_code, target_class)
    tree = ast.parse(source_code)
    analyzer = IVMCAnalyzer()
    analyzer.visit(tree)

    field_methods = analyzer.class_field_usage.get(target_class)
    if field_methods is None:
        return None

    return {field: (len(methods) / class_nom) * 100 for field, methods in field_methods.items()}
