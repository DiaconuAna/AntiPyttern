"""
Switch Statement - function-level
CC of function >= 10
"""
import ast
from metrics.cyclomatic_complexity import *

def check_switch_stmt_smell_func_level(source_code: str, function_name: str) -> bool:
    return get_function_cc(source_code, function_name) >= 10


def check_switch_stmt_smell(source_code: str) -> bool:
    """
    Checks presence of switch statement code smell in source code of a file
    :param source_code:
    :return:
    """
    for node in ast.walk(ast.parse(source_code)):
        if isinstance(node, ast.FunctionDef) and check_switch_stmt_smell_func_level(source_code, node.name):
            return True
    return False
