import re
from pathlib import Path
from typing import Literal

import requests
import typer

AOC_DIR = Path(__file__).parent.parent


class AdventOfCodeClient:
    base_url = "https://adventofcode.com"

    def __init__(self, session: requests.Session) -> None:
        self.session = session
        template_file = AOC_DIR / "lib" / "solution_starter.py"
        self.template_text = template_file.read_text().strip()
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

    def get_questions(self, year: int, day: int) -> list[str]:
        problem_text = self.get_puzzle_text(year, day)
        return re.findall(r"<em>(.*?\?)</em>", problem_text)

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

    def _get_day_block(self, year: int, day: int) -> str:
        title = self.get_puzzle_title(year, day)
        url = self._get_day_url(year, day)
        lines = [
            f'    print("--- {title} ---")',
            f'    print("{url}")',
        ]
        return "\n".join(lines)

    def _get_part_block(self, year: int, day: int, part: Literal[1, 2]) -> str:
        questions = self.get_questions(year, day)
        answers = self.get_answers(year, day)
        question = questions[part - 1] if len(questions) >= part else ""
        answer = answers[part - 1] if len(answers) >= part else ""
        lines = [
            f'    print("({part}) {question}")',
            f"    part_{part} = solver.solve_part_{part}()",
            f'    print("Solution: " + str(part_{part}))',
        ]
        if answer:
            lines.append(f'    print("Expected: {answer}")')
        else:
            lines.append(f"    copy_to_clipboard(part_{part})")
        return "\n".join(lines)

    def _get_suffix(self, year: int, day: int) -> str:
        return "\n\n".join(
            [
                self._get_day_block(year, day),
                self._get_part_block(year, day, 1),
                self._get_part_block(year, day, 2),
            ]
        )

    def _get_starter_solution(self, year: int, day: int) -> str:
        docstring = "\n".join(
            [
                f'"""{self.get_puzzle_title(year, day)}',
                self._get_day_url(year, day),
                '"""',
            ]
        )
        return "\n\n".join(
            [
                docstring,
                self.template_text,
                self._get_suffix(year, day),
            ]
        )

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

    def append_suffix(self, year: int, day: int) -> None:
        solution_file = AOC_DIR / f"y{year}" / f"day{day:02}" / "solve.py"
        file_text = solution_file.read_text()
        suffix = self._get_suffix(year, day)
        if suffix in file_text:
            print(f"Suffix is already present for {solution_file}")
            return
        with solution_file.open("a") as f:
            f.write("\n\n" + suffix)

    def create_starter(self, year: int, day: int) -> None:
        self.write_input_file(year, day)
        self.write_solution_starter(year, day)

    def get_cli_app(self) -> typer.Typer:
        app = typer.Typer()
        app.command()(self.write_input_file)
        app.command()(self.write_solution_starter)
        app.command()(self.append_suffix)
        return app
