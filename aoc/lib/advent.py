import re
from pathlib import Path

import requests
import typer

AOC_DIR = Path(__file__).parent.parent


class AdventOfCodeClient:
    base_url = "https://adventofcode.com"

    def __init__(self, session: requests.Session) -> None:
        self.session = session
        template_file = AOC_DIR / "lib" / "solution_starter.py"
        self.template_text = template_file.read_text()
        self._puzzle_cache = {}

    def _get_day_url(self, year: int, day: int) -> str:
        return f"{self.base_url}/{year}/day/{day}"

    def get_puzzle_text(self, year: int, day: int) -> str:
        if (year, day) in self._puzzle_cache:
            return self._puzzle_cache[(year, day)]
        url = self._get_day_url(year, day)
        text = self.session.get(url, timeout=10).text
        self._puzzle_cache[(year, day)] = text
        return text

    def get_puzzle_input(self, year: int, day: int) -> str:
        url = self._get_day_url(year, day) + "/input"
        return self.session.get(url, timeout=10).text

    def get_puzzle_title(self, year: int, day: int) -> str:
        problem_text = self.get_puzzle_text(year, day)
        return list(re.findall(r"<h2>--- (Day \d+: .*?) ---</h2>", problem_text))[0]

    def get_answers(self, year: int, day: int) -> list[str]:
        problem_text = self.get_puzzle_text(year, day)
        return re.findall(r"Your puzzle answer was <code>(.*?)</code>", problem_text)

    @staticmethod
    def _already_started(path: Path) -> bool:
        return path.exists() and path.read_text().strip() != ""

    def _write_if_not_exists(self, path: Path, value: str) -> None:
        if self._already_started(path):
            print("Path already exists: " + str(path))
            return
        with path.open("w") as f:
            f.write(value)

    def _get_starter_solution(self, year: int, day: int) -> str:
        docstring = "\n".join(
            [
                f'"""{self.get_puzzle_title(year, day)}',
                self._get_day_url(year, day),
                '"""',
            ]
        )
        starter = docstring + "\n\n" + self.template_text
        answers = self.get_answers(year, day)
        if answers:
            answer_string = ", ".join(answers)
            starter += f'\n\n    print("Expected answers: {answer_string}")'
        return starter

    def write_input_file(self, year: int, day: int) -> None:
        self._write_if_not_exists(
            AOC_DIR / f"y{year}" / f"day{day:02}" / "input.txt",
            self.get_puzzle_input(year, day),
        )

    def write_solution_starter(self, year: int, day: int) -> None:
        self._write_if_not_exists(
            AOC_DIR / f"y{year}" / f"day{day:02}" / "solve.py",
            self._get_starter_solution(year, day),
        )

    def create_starter(self, year: int, day: int) -> None:
        self.write_input_file(year, day)
        self.write_solution_starter(year, day)

    def get_cli_app(self) -> typer.Typer:
        app = typer.Typer()
        app.command()(self.write_input_file)
        app.command()(self.write_solution_starter)
        return app
