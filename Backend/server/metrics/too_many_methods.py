import subprocess
import json
import sys
import os
from dotenv import load_dotenv

def run_pylint(file_path):
    """Run pylint checking for too-many-public-methods."""
    load_dotenv()

    pylintrc_path = os.getenv('PYLINTRC_PATH')
    if not pylintrc_path:
        print("Error: PYLINTRC_PATH not found in .env file")
        sys.exit(1)

    try:
        result = subprocess.run([
            'pylint',
            f'--rcfile={pylintrc_path}',
            '--output-format=json',
            '--disable=all',
            '--enable=too-many-public-methods',
            file_path
        ], capture_output=True, text=True, check=False)

        if result.returncode not in (0, 4, 8, 16, 32):
            print(f"Unexpected pylint error: {result.stderr}")
            sys.exit(1)

        return json.loads(result.stdout)

    except Exception as e:
        print(f"Failed to run pylint: {e}")
        sys.exit(1)


def extract_classes(pylint_output):
    """Extract class names with too many public methods."""
    classes = {}

    for entry in pylint_output:
        if entry['message-id'] == 'R0904':  # too-many-public-methods
            class_name = entry['obj']
            classes[class_name] = True

    return classes


def compute_nom_for_class_in_file(filename, target_class_name):
    """Check if a given class has too many public methods."""
    classes = {}
    pylint_output = run_pylint(filename)
    for entry in pylint_output:
        if entry['message-id'] == 'R0904' and entry['obj'] == target_class_name:  # too-many-public-methods
            return True

    return False
