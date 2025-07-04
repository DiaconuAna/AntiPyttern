import subprocess
import re
import sys
import logging

logger = logging.getLogger(__name__)

def get_lcom4(file_path, class_name):
    """
    Computes the cohesion of a class using LCOM4
    :param file_path:
    :param class_name:
    :return:
    """
    try:
        result = subprocess.run(["lcom", file_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.warning(f"lcom failed: {e.stderr}")
        return 0

    for line in result.stdout.splitlines():
        line = line.strip()
        match = re.match(r"\|\s+(.*?)\s+\|\s+(\d+)\s+\|", line)
        if match:
            full_class_path, lcom_score = match.groups()
            if full_class_path.endswith(f".{class_name}"):
                logger.debug(f"{full_class_path} -> {lcom_score}")
                return int(lcom_score)

    logger.debug(f"Class '{class_name}' not found in {file_path}.")
    return 0
