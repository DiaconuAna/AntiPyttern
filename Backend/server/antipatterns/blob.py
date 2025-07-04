from code_smells.large_class import *
from code_smells.long_method import *
from code_smells.feature_envy import *
from code_smells.data_class import *
from metrics.cohesion import *
from metrics.lines_of_code import code_comment_ratio
from antipatterns.utils import *

import logging

logger = logging.getLogger(__name__)


def is_blob_controller(file_name, source_code, class_node, config):
    """
    Checks if a given class node is a potential Blob controller class
    Detection heuristic:
     * Large Class smell &
     * at least one long method &
     * [ switch statement smell ] &
     * envy ratio (to measure its link to the dataclasses) &
     * low cohesion
    """
    smell_detectors = {
        "large_class": lambda: check_large_class_smell(file_name, source_code, class_node),
        "low_cohesion": lambda: get_lcom4(file_name, class_node.name) >= 1,
        "long_method": lambda: check_long_method_smell(source_code, class_node),
        "feature_envy": lambda: check_feature_envy_smell(class_node),
        "comment_heavy": lambda: code_comment_ratio(source_code, class_node.name) > 0.25
    }

    score = 0
    present_smells = {}
    for smell_name, props in config["smells"].items():
        present = smell_detectors[smell_name]()
        present_smells[smell_name] = present

        logger.debug(f"\tBLOB -> {smell_name}: {present}")

        if props["required"] and not present:
            return False, present_smells

        if present:
            score += props["weight"]

    logger.debug(f"Total score: {score}")
    return score >= config["threshold"], present_smells


def is_blob_antipattern(file_path):
    """
    Checks whether Blob antipattern occurs at file level
    - find the controller classes => warn the user about their potential to become a Blob controller
    - find the data classes => warn the user about their potential to become data classes for a Blob object
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    config = load_heuristic_config("antipatterns/config/blob_ctrl_smell_weights.yaml")

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            val = is_blob_controller(file_path, source_code, node, config)
            if val:
                logger.info(f"Class {node.name} is a Blob controller class.")
            if check_dataclass_smell(node):
                logger.info(f"Class {node.name} has potential to become a Blob data class: {check_dataclass_smell(node)}")


def is_blob_antipattern_to_json(file_path):
    """
    Analyze a file and return JSON-formatted details about class-level antipatterns.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    config = load_heuristic_config("antipatterns\\config\\blob_ctrl_smell_weights.yaml")

    results = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            is_blob_ctrl, smells = is_blob_controller(file_path, source_code, node, config)
            is_data_class = check_dataclass_smell(node)

            if is_blob_ctrl or is_data_class:
                results.append({
                    "class_name": node.name,
                    "is_data_class": is_data_class,
                    "is_blob_controller": is_blob_ctrl,
                    "blob_smells": smells
                })

    return json.dumps({
        "file": os.path.basename(file_path),
        "classes": results
    }, indent=2)
