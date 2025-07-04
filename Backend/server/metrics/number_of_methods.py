import ast

def compute_number_of_methods(class_node):
    """
    Computes the number of methods present in the given class.
    Excludes magic methods.
    """
    method_count = 0
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef):
            if not (node.name.startswith('__') and node.name.endswith('__')):
                method_count += 1

    return method_count


def compute_nom_in_file(filename):
    """
    Parse a Python file and return a dictionary: {class_name: method_count}
    :param filename:
    :return:
    """
    with open(filename, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())

    nom_per_class = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            nom_per_class[node.name] = compute_number_of_methods(node)

    return nom_per_class


def compute_nom_for_class(source_code, target_class):
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == target_class:
            return compute_number_of_methods(node)

    return -1
