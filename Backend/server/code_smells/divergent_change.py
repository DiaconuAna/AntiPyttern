"""
Code smell that is harder to detect for a static analysis tool since no version control is performed

But in a more static setup, I would say it is characterized by the following:

A class is more likely to exhibit Divergent Change if:
- low cohesion between methods of a class
- the class has too many methods
"""
from metrics.cohesion import *
from metrics.too_many_methods import compute_nom_for_class_in_file
import logging


logger = logging.getLogger(__name__)


def check_divergent_change(file_path, class_node):
    methods: int = compute_nom_for_class_in_file(file_path, class_node.name)
    lcom: int = get_lcom4(file_path, class_node.name)

    if lcom is None:
        logger.warning(f"LCOM4 could not be computed for class '{class_node.name}' in file '{file_path}'. Skipping divergent change check.")
        return False

    return methods > 0 and lcom >= 1
