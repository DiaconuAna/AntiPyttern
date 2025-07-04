import subprocess
import logging
import os
import re
import ast

logger = logging.getLogger(__name__)

def normalize_path(path):
    return os.path.normpath(path).replace("\\", "/").lower()

def check_unused_file(project_path, file_path):
    """
    Check if a file in a project contains unused code.
    :param project_path:
    :param file_path:
    :return:
    """
    result = subprocess.run(
        ["vulture", project_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    file_to_find = normalize_path(file_path)
    for line in result.stdout.splitlines():
        match = re.match(r"^(.*?):\d+:", line)
        if match:
            file_part = match.group(1)
            norm_path = normalize_path(file_part)
            if norm_path == file_to_find:
                return True

    return False

def check_unused_construct(project_path, construct_name):
    """
    Checks if a specific construct in a project contains unused code.
    :param project_path:
    :param construct_name:
    :return:
    """
    try:
        result = subprocess.run(
            ["vulture", project_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in result.stdout.splitlines():
            if construct_name in line:
                return True

    except FileNotFoundError:
        logger.error("Vulture is not installed. Install with: pip install vulture")
    return False


def check_unused_methods_in_class(project_path, class_node):
    unused_methods = []

    for node in class_node.body:
        if isinstance(node, ast.FunctionDef):
            method_name = node.name
            if check_unused_construct(project_path, method_name):
                unused_methods.append(method_name)

    return unused_methods
