"""
Data class code smell metric inspired from Mantyla
In a data class, each field should contain, at most, a getter and setter.
If a class contains at least a method that is not a getter or setter => the class IS NOT a data class.

A Data Class smell

AND Python-specific

@dataclass annotation -> semantic indicator of the data class code smell
-> can be detected using ast
"""
from metrics.is_getter_setter import is_getter_setter
import ast

def check_dataclass_decorator(class_node):
    for decorator in class_node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
            return True
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name) and decorator.func.id == "dataclass":
                return True
    return False


def check_getters_setters(class_node):
    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and is_getter_setter(node) == False:
            return False
    return True


def check_dataclass_smell(class_node):
    """
    A class is a data class bad smell if over 70% of its methods are getters and setters
    :param class_node:
    :return:
    """
    function_count = 0
    getter_setter_count = 0
    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_count += 1
            getter_setter_count += 1 if is_getter_setter(node) else 0

    return function_count == 0 or (getter_setter_count / function_count) * 100 > 70
