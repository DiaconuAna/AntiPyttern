import abc
import ast

def analyze_class_interfaces(cls):
    formal_interfaces = 0
    informal_interfaces = 0
    base_names = []

    for base in cls.__bases__:
        if base is object:
            continue
        base_names.append(base.__name__)

        if issubclass(base, abc.ABC):
            formal_interfaces += 1

        informal_interfaces += 1

    return {
        'class': cls.__name__,
        'formal_abc_count': formal_interfaces,
        'informal_base_count': informal_interfaces,
        'base_names': base_names,
    }

def is_multi_interface_class(cls):
    """
    Determines if a class implements multiple interfaces (formal or informal),
    based on defined thresholds.

    :param cls: The class object to analyze.
    :return: True if the class is considered to implement many interfaces, False otherwise.
    """
    analysis = analyze_class_interfaces(cls)
    return (
            analysis['formal_abc_count'] >= 2 or
            analysis['informal_base_count'] >= 3
    )


def analyze_ast_class_interfaces(class_node):
    """
    Analyzes an AST ClassDef node to estimate how many interfaces (base classes) it implements.
    Since we're using AST, we can't detect if a base is an ABC—only count total base classes.

    :param class_node: ast.ClassDef
    :return: dict with estimated interface metrics
    """
    base_names = []

    for base in class_node.bases:
        if isinstance(base, ast.Name):
            base_names.append(base.id)
        elif isinstance(base, ast.Attribute):
            base_names.append(base.attr)

    return len(base_names) > 0
