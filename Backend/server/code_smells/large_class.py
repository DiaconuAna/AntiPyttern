"""
Large Class Code Smell
LOC > 100 OR too many methods OR too many attributes
"""

from metrics.lines_of_code import *
from metrics.too_many_methods import *
from metrics.too_many_attributes import *

from typing import Any
import logging

logger = logging.getLogger(__name__)


def check_large_class_smell(file_name: str, source_code: str, class_node: Any) -> bool:
    loc: int = get_class_loc(source_code, class_node.name)
    methods: int = compute_nom_for_class_in_file(file_name, class_node.name)
    attributes: int = compute_nof_for_class_in_file(file_name, class_node.name)

    logger.debug(f"loc={loc}, methods={methods}, attributes={attributes}, class_name={class_node.name}")

    if loc > 100 or methods > 0 or attributes > 0:
        return True
    return False
