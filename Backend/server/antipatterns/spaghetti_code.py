from code_smells.switch_stmt import *
from code_smells.long_method import *
from metrics.check_unused import *
from metrics.global_usage import *
from antipatterns.utils import *

import logging
import os
import json

logger = logging.getLogger(__name__)

def is_spaghetti_code(project_path, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    config = load_heuristic_config("antipatterns/config/spaghetti_code_weights.yaml")

    has_long_method_no_param = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and check_long_method_no_params(source_code, node):
            has_long_method_no_param = True
            break

    smell_detectors = {
        "long_methods_no_params": has_long_method_no_param,
        "global_vars": count_global_warnings(file_path) > 0,
        "switch_stmt": check_switch_stmt_smell(source_code),
        "dead_code": check_unused_file(project_path, file_path)
    }

    logger.debug(f"{file_path} - {smell_detectors}")

    score = 0.0
    for smell_name, props in config["smells"].items():
        if smell_detectors[smell_name]:
            score += props["weight"]

    thresholds = config.get("thresholds", {})
    potential_threshold = thresholds.get("potential_spaghetti_code", 0.4)
    confirmed_threshold = thresholds.get("spaghetti_code", 0.6)

    logger.debug(f"Score: {score} for file {file_path}")

    if score >= confirmed_threshold:
        logger.info(f"File {file_path} exhibits Spaghetti Code symptoms.")
        spaghetti_type = "spaghetti"
    elif score >= potential_threshold:
        logger.info(f"File {file_path} shows potential for Spaghetti Code.")
        spaghetti_type = "potential"
    else:
        spaghetti_type = "clean"

    return spaghetti_type, score, smell_detectors


def is_spaghetti_code_to_json(project_path, file_path):
    spaghetti_type, score, smells = is_spaghetti_code(project_path, file_path)
    return json.dumps({
        "file": os.path.basename(file_path),
        "classification": spaghetti_type,
        "score": score,
        "spaghetti_smells": smells
    }, indent=2)


