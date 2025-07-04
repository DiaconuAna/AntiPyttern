"""
IVMC <= 1 (Munro)
OR
Usage Ratio < 10% (Rasool)
"""
from metrics.ivmc import *

import logging
logger = logging.getLogger(__name__)

def check_temporary_field_smell(source_code, class_node):
    class_ivmc = compute_ivmc_per_class(source_code, class_node.name)
    class_usage_ratio = compute_field_usage_percentage_per_class(source_code, class_node.name)

    logger.info(class_ivmc)
    logger.info(class_usage_ratio)
    if class_ivmc is not None:
        if any(value == 1 for value in class_ivmc.values()):
            logger.info("IVMC: At least one field is used by exactly one method!")
            return True
        else:
            logger.debug("IVMC: No field is used by exactly one method.")

    if class_usage_ratio is not None:
        if any(value <= 10 for value in class_usage_ratio.values()):
            logger.info("Usage ratio: smaller than 10%")
            return True
        else:
            logger.debug("Usage ratio: larger than 10%")

    return False
