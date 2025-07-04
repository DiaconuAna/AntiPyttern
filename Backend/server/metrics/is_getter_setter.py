"""
A function is a getter or setter if it accesses or sets attributes of self.
It should contain no calls, math, logic or external references.

Assumption: CC should be 1 so no checks for control structures will be performed
"""
import ast

def is_getter_setter(function):
    if not isinstance(function, ast.FunctionDef):
        return False

    allowed_nodes = (ast.Return, ast.Assign, ast.Expr, ast.Load, ast.Store, ast.Attribute, ast.Name)

    for node in ast.walk(function):
        if isinstance(node, ast.arguments): # function arguments are skipped
            continue

        if isinstance(node, ast.Call): # Function calls are disallowed (e.g., self.other.get_x())
            return False

        if isinstance(node, (ast.BinOp, ast.BoolOp, ast.Compare)): # Binary operations are disallowed (a + b, a > b, etc.)
            return False

        if isinstance(node, ast.Attribute):
            if not (isinstance(node.value, ast.Name) and node.value.id == "self"):
                return False

    return True
