import sys
from pathlib import Path


def get_input_path(main_file: str) -> Path:
    filename = sys.argv[1] if len(sys.argv) > 1 else "input"
    filepath = Path(main_file).parent / f"{filename}.txt"
    return filepath


# FIXME
def ansify(*args, **kwargs) -> str:
    return ""
