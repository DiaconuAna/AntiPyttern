import subprocess
import sys
import re

import logging

logger = logging.getLogger(__name__)

GLOBAL_WARNINGS = {"W0601", "W0602", "W0603", "W0604"}

"""
global-variable-undefined / W0601 - Used when a variable is defined through the "global" statement but the variable is not defined in the module scope.
global-variable-not-assigned / W0602 - When a variable defined in the global scope is modified in an inner scope,
                                       the 'global' keyword is required in the inner scope only if there is an assignment
                                       operation done in the inner scope.
global-statement / W0603 - Used when you use the "global" statement to update a global variable. Pylint discourages its usage.
                           That doesn't mean you cannot use it!
global-at-module-level / W0604 - Used when you use the "global" statement at the module level since it has no effect.
"""

def count_global_warnings(file_path):
    try:
        result = subprocess.run(
            ["pylint", "--disable=all", "--enable=W0601,W0602,W0603,W0604", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        count = 0
        for line in result.stdout.splitlines():
            match = re.search(r"\b(W060[1-4])\b", line)
            if match:
                count += 1

        return count

    except FileNotFoundError:
        logger.error("pylint not found. Please make sure it is installed and available in PATH.")
        return 0
