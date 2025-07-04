"""
If external field access > internal field access (aka external field access / (internal field access + 1)) >= 1
"""

import logging
from typing import Any

from metrics.attributes import *

logger = logging.getLogger(__name__)

def check_feature_envy_smell(class_node: Any):
    logger.debug(f"\nClass: {class_node.name}")
    detector = FieldAccesses(class_node)
    internal, external = detector.analyze()

    total_methods = len(internal)
    smelly_methods = 0

    for method in sorted(internal):
        i = internal[method]
        e = external[method]
        ratio = e / (i + 1)

        if ratio >= 1.0 and e >= 2:
            smelly_methods += 1
            logger.debug(f"Method '{method}': Internal={i} External={e} EnvyRatio={ratio:.2f} [SMELL]")
        else:
            logger.debug(f"Method '{method}': Internal={i} External={e} EnvyRatio={ratio:.2f}")

    if total_methods > 0:
        class_ratio = smelly_methods / total_methods
        logger.debug(f"--> {smelly_methods}/{total_methods} methods smelly ({class_ratio:.0%})")
        if class_ratio >= 30:
            return True

    return False
