import sys
import datetime
import importlib
from pathlib import Path
from typing import Tuple
from types import ModuleType


def get_inputs() -> Tuple[int, int]:
    args = sys.argv
    try:
        year, day = int(args[1]), int(args[2])
        return year, day
    except IndexError as e:
        print(
            "Invalid system arguments: Enter exactly two arguments for 'year' and 'day'."
        )
    except ValueError as e:
        print("Invalid system arguments: 'year' and 'day' must be integers.")
    print("Defaulting to today's year and date.")
    today = datetime.date.today()
    year = today.year
    day = today.day
    return year, day


def load_module(day: int, year: int) -> ModuleType:
    year_dir = Path(f"y{year}")
    for day_dir in year_dir.iterdir():
        day_prefix = f"day_{day:02}"
        if day_dir.stem.startswith(day_prefix):
            module_name = ".".join([*day_dir.parts, "main"])
            module = importlib.import_module(module_name)
            return module
    return None


def copy_to_clipboard(answer_1, answer_2) -> None:
    text = ""
    if answer_1 is not None:
        text = str(answer_1)
    if answer_2 is not None:
        text = str(answer_2)
    try:
        import pyperclip

        pyperclip.copy(text)
    except ModuleNotFoundError as e:
        print("The module pyperclip is not installed.")


year, day = get_inputs()
mod = load_module(day, year)
answer_1, answer_2 = mod.solution()
copy_to_clipboard(answer_1, answer_2)
print(f"Part 1 solution: {answer_1}")
print(f"Part 2 solution: {answer_2}")
