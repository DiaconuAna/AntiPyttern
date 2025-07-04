"""
Utility to count the number of Python files in a GitHub repository, per folder,
with optional exclusion of multiple folder paths. Also computes average LOC and class count.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from collections import defaultdict

def count_python_files(github_url, exclude_folders=None):
    if exclude_folders:
        exclude_folders = {folder.strip().strip("/") for folder in exclude_folders.split(",") if folder.strip()}
    else:
        exclude_folders = set()

    with tempfile.TemporaryDirectory() as tmpdirname:
        try:
            print(f"Cloning repository from {github_url}...")
            subprocess.run(["git", "clone", github_url, tmpdirname], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print("Failed to clone the repository. Please check the URL.")
            return

        all_py_files = list(Path(tmpdirname).rglob("*.py"))

        def is_excluded(path):
            rel_parts = path.relative_to(tmpdirname).parts
            for i in range(1, len(rel_parts) + 1):
                sub_path = "/".join(rel_parts[:i])
                if sub_path in exclude_folders:
                    return True
            return False

        # Filter Python files based on exclusion rules
        python_files = [f for f in all_py_files if not is_excluded(f)]

        # Count files, LOC, and classes per folder
        file_counts = defaultdict(int)
        loc_counts = defaultdict(int)
        class_counts = defaultdict(int)

        total_loc = 0
        total_classes = 0

        for file_path in python_files:
            rel_path = file_path.relative_to(tmpdirname)
            folder = str(rel_path.parent)

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                non_empty_lines = [line for line in lines if line.strip()]
                loc = len(non_empty_lines)
                class_count = sum(1 for line in lines if line.strip().startswith("class "))

            file_counts[folder] += 1
            loc_counts[folder] += loc
            class_counts[folder] += class_count
            total_loc += loc
            total_classes += class_count

        print(f"\nPython file counts per folder"
              f"{' (excluding: ' + ', '.join(sorted(exclude_folders)) + ')' if exclude_folders else ''}:")
        for folder in sorted(file_counts.keys()):
            files = file_counts[folder]
            avg_loc = loc_counts[folder] / files if files > 0 else 0
            avg_classes = class_counts[folder] / files if files > 0 else 0
            print(f"{folder or '.'}: {files} file(s), avg LOC: {avg_loc:.2f}, avg classes: {avg_classes:.2f}")

        total_files = len(python_files)
        overall_avg_loc = total_loc / total_files if total_files > 0 else 0
        overall_avg_classes = total_classes / total_files if total_files > 0 else 0

        print(f"\nTotal: {total_files} Python file(s)")
        print(f"Overall LOC: {total_loc}")
        print(f"Overall average LOC per file: {overall_avg_loc:.2f}")
        print(f"Total class definitions: {total_classes}")
        print(f"Overall average classes per file: {overall_avg_classes:.2f}")

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ").strip()
    exclude = input("Enter folder paths to exclude (comma-separated, e.g. tests,examples/tutorial): ").strip()

    if not repo_url:
        print("Repository URL cannot be empty.")
    else:
        count_python_files(repo_url, exclude_folders=exclude)
