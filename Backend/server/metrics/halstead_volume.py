from radon.metrics import h_visit_ast
import ast

def get_function_halstead_volume_from_file(source_code: str, function_name: str) -> float:
    """
    Get Halstead Volume of a specific function from Python code
    """
    tree = ast.parse(source_code)
    results = h_visit_ast(tree)

    for function_report in results.functions:
        if function_report[0] == function_name:
            return function_report[1].volume

    return -1
