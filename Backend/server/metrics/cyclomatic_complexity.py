from radon.complexity import cc_visit

def get_function_cc(source_code: str, function_name: str) -> int:
    """
    Get the Cyclomatic Complexity (CC) of a specific function from source code.
    """
    blocks = cc_visit(source_code)
    for block in blocks:
        if block.name == function_name:
            return block.complexity
    return -1
