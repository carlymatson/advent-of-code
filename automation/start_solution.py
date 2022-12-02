import sys
import shutil
import datetime
from pathlib import Path
from typing import Tuple

from automation.scrape import scrape_my_input

TEMPLATE_PATH = Path(__file__).parent / "template.py"


def create_solution_starter(year: int, day: int) -> None:
    year_dir = Path(f"y{year}")
    day_dir = year_dir / f"day_{day:02}"
    print(f"Creating directory {day_dir}...")
    try:
        day_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass

    # Create starter solution from template.
    print(f"Creating starter solution file...")
    solution_path = day_dir / "main.py"
    if not solution_path.exists():
        shutil.copy(str(TEMPLATE_PATH), str(solution_path))

    # Create __init__.py
    init_path = day_dir / "__init__.py"
    if not init_path.exists():
        init_path.touch()
        with open(init_path, "w") as f:
            f.write("from . import main")

    # Write my input to file.
    print("Copying individual input file...")
    try:
        my_input = scrape_my_input(year, day)
    except Exception as e:
        print("Problem occurred while scraping input.")
        print(e)
        my_input = ""
    input_path = day_dir / "input.txt"
    with open(input_path, "w") as f:
        f.write(my_input)
    print("Done!")


def parse_sys_args() -> Tuple[int, int]:
    args = sys.argv
    try:
        year, day = int(args[1]), int(args[2])
    except Exception as e:
        today = datetime.date.today()
        year = today.year
        day = today.day
    return year, day


if __name__ == "__main__":
    year, day = parse_sys_args()
    create_solution_starter(year, day)
