"""
Based on Mantyla's description of a polynomial metric involving LOC, CC and Halstead metrics
(LOC > 50 AND CC > 5) OR (Halstead Volume > 800)
"""

from metrics.lines_of_code import *
from metrics.cyclomatic_complexity import *
from metrics.halstead_volume import *

from typing import Any
import logging

logger = logging.getLogger(__name__)

def is_long_method(source_code, function_node):
    loc = get_function_loc(source_code, function_node.name)
    cc = get_function_cc(source_code, function_node.name)
    halstead_volume = get_function_halstead_volume_from_file(source_code, function_node.name)

    return (loc > 50 and cc > 5) or halstead_volume > 800


def has_no_parameters(function_node):
    args = function_node.args
    return (
        len(args.args) == 0 and
        len(args.kwonlyargs) == 0 and
        args.vararg is None and
        args.kwarg is None
    )


def check_long_method_no_params(source_code, function_node):
    return is_long_method(source_code, function_node) and has_no_parameters(function_node)


def check_long_method_smell(source_code, class_node):
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef):
            return is_long_method(source_code, node)
    return False
