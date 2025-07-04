import yaml

def load_heuristic_config(yaml_path):
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

