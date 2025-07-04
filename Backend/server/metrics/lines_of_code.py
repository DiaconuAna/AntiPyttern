import ast
from radon.raw import analyze

def get_class_sloc(source_code):
    """
    Computes the SLOC - source lines of code - using radon.
    SLOC - lines excluding blank lines and comments
    :param source_code:
    :return:
    """
    radon_metrics = analyze(source_code)
    return radon_metrics.sloc


def get_class_comments(source_code):
    """
    Computes the number of Python comments
    :param source_code:
    :return:
    """
    radon_metrics = analyze(source_code)
    return radon_metrics.comments


def code_comment_ratio(source_code, class_name):
    """
    C + M % L = total comment density (single + multi line comms) as of LOC
    :param source_code:
    :return:
    """

    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            metrics = analyze(source_code)

            loc = metrics.loc
            cloc = metrics.comments
            mloc = metrics.multi

            return (cloc + mloc) / loc if loc > 0 else 0
    return 0


def get_classes_with_loc(file_path):
    """Parse file using AST and compute LOC for each class safely."""
    classes = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source, filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            start_line = node.lineno
            end_line = getattr(node, 'end_lineno', None)

            if end_line is not None:
                loc = end_line - start_line + 1
                classes[class_name] = loc
            else:
                classes[class_name] = 0

    return classes


def get_class_loc(source_code, class_name):
    """Return LOC for a given class in a given Python file."""

    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            start_line = node.lineno
            end_line = getattr(node, 'end_lineno', None)
            if end_line is not None:
                return end_line - start_line + 1

    return 0


def get_function_loc(source_code, function_name):
    """Return LOC for a given function in a given Python source code."""

    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            first_line = node.lineno
            last_line = max(
                getattr(child, 'lineno', first_line) for child in ast.walk(node)
            )
            return last_line - first_line + 1

    raise ValueError(f"Function '{function_name}' not found.")
