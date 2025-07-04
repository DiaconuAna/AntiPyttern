import ast
import logging
import os
import json

from metrics.check_unused import check_unused_methods_in_class
from metrics.cohesion import get_lcom4
from metrics.too_many_methods import compute_nom_for_class_in_file
from metrics.class_interfaces import analyze_ast_class_interfaces

from antipatterns.utils import load_heuristic_config

logger = logging.getLogger(__name__)

def is_swiss_army_knife(project_path, file_path, class_node, config):
    smell_detectors = {
        "large_class": compute_nom_for_class_in_file(file_path, class_node.name),
        "speculative_gen": check_unused_methods_in_class(project_path, class_node),
        "cohesion": (get_lcom4(file_path, class_node.name) >= 2) or (get_lcom4(file_path, class_node.name) == 0),
        "interfaces": analyze_ast_class_interfaces(class_node),
    }

    logger.info(smell_detectors)

    score = 0
    for smell_name, props in config["smells"].items():
        if smell_detectors[smell_name]:
            score += props["weight"]

    thresholds = config.get("thresholds", {})
    potential_threshold = thresholds.get("potential_sak", 0.5)
    confirmed_threshold = thresholds.get("sak", 0.8)

    logger.debug(f"Score: {score} for file {file_path}")

    if score >= confirmed_threshold:
        logger.info(f"File {file_path} exhibits Swiss Army Knife symptoms.")
        sak_type = "sak"
    elif score >= potential_threshold:
        logger.info(f"File {file_path} shows potential for Swiss Army Knife.")
        sak_type = "potential"
    else:
        sak_type = "clean"

    return sak_type, score, smell_detectors


def is_sak_to_json(project_path, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    config = load_heuristic_config("antipatterns/config/swiss_army_knife_weights.yaml")

    results = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            sak_type, score, smells = is_swiss_army_knife(project_path, file_path, node, config)
            if sak_type != "clean":
                results.append({
                "class": node.name,
                "classification": sak_type,
                "score": score,
                "smells": smells,
            })

    logger.info(results)

    return json.dumps({
        "file": os.path.basename(file_path),
        "results": results
    }, indent=2)
