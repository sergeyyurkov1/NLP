import os
import sys

from ruamel.yaml import YAML

yaml = YAML(typ="rt", pure=True)
yaml.preserve_quotes = True
yaml.default_flow_style = False


def get_models() -> list[str]:
    return sorted(
        [
            i.replace("_", "")
            for i in os.listdir(path="models")
            if not i.startswith("__") and os.path.isdir(os.path.join("models", i))
        ]
    )


def read_yaml(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.load(f)

    except FileNotFoundError:
        print(f"{path} is not found. Exiting.")
        sys.exit()


def write_yaml(path: str, data: dict) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
    except Exception as e:
        print(e)
        sys.exit()
