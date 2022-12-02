import re
import time
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

# Create files for all of these and pre-populate! Hooray!

BASE_URL = "https://adventofcode.com"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
session_id = "53616c7465645f5f5e1f5479a37c878da404e3469bd5c9bc0992de7b044a236ee2553b3066efcdb1d6adba4e0748b89ea9ff985a080663aeb221d7b0bb0010da"


def get_day_url(year: int, day: int) -> str:
    url = f"{BASE_URL}/{year}/day/{day}"
    return url


def scrape_link(url: str) -> str:
    cookies = {"session": session_id}
    headers = {"User-Agent": user_agent}
    r = requests.get(url, cookies=cookies, headers=headers)
    try:
        content = r.content.decode("utf-8")
        return content
    except Exception as e:
        print(e)
        return None


def scrape_my_input(year: int, day: int) -> str:
    base_url = get_day_url(year, day)
    input_url = base_url + "/input"
    text = scrape_link(input_url)
    return text


def scrape_all_inputs() -> Dict[Tuple[int, int], str]:
    daily_inputs = {
        (year, day): my_input
        for year in range(2019, 2023)
        for day in range(1, 26)
        if (my_input := scrape_my_input(year, day)) is not None
    }
    return daily_inputs


def extract_header(soup: BeautifulSoup) -> str:
    h2_headers = soup.find_all("h2")
    try:
        day_header = h2_headers[0]
    except Exception as e:
        print(f"No header found for {url}!")
        return None
    title = day_header.get_text()
    title = title.strip("- ")
    return title


def get_day_header(url: str) -> str:
    result = requests.get(url)
    slow_down = True
    if slow_down:
        time.sleep(0.2)
        print(".", end="", flush=True)
    soup = BeautifulSoup(result.content, "html.parser")
    return extract_header(soup)


def pythonify_day_header(s: str) -> str:
    if s.startswith("Day "):
        s = s[4:]
    day, title = s.split(": ", 1)
    day = int(day)
    title = re.sub("[-!']", "", title)
    title = re.sub(" ", "_", title)
    pythonified = f"day_{day:02}__{title.lower()}"
    return pythonified


def create_day_file(year: int, day_header: str) -> None:
    dir_name = pythonify_day_header(day_header)
    path = Path(f"f{year}", dir_name)
    path.mkdir(parents=True, exist_ok=True)


def create_solution_template(year: int, day: int) -> None:
    # Get filepath name
    # Create
    # Copy contents of "template.py" to file
    pass


def write_day_header_to_readme(year: int, day_title: str) -> None:
    year_filepath = Path(f"y{year}.md")
    with open(year_filepath, "a") as f:
        f.write(" - " + day_title)


def create_all():
    for year in range(2019, 2022):
        for day in range(1, 26):
            url = f"{BASE_URL}/{year}/day/{day}"
            day_header = get_day_header(url)
            create_day_file(year, day_header)


def has_answer(tag):
    try:
        s = tag.contents[0].string
        return "answer was" in s
    except Exception as e:
        return False


def adhoc(soup):
    print(extract_header(soup))
    return
    result = soup.find_all(has_answer)
    n = len(result)
    answers = [tag.contents[1].string for tag in result] + [None] * (2 - n)
    print(answers)
    # for tag in result:
    # code = tag.contents[1]
    # print(code.string)


if __name__ == "__main__":
    days = [(year, day) for year in (2019, 2020, 2021) for day in range(1, 26)]
    for year, day in days:
        url = get_day_url(year, day)
        site = scrape_link(url)
        soup = BeautifulSoup(site, "html.parser")
        adhoc(soup)
        # header = extract_header(soup)
        # print("-" * 5)
        # print(f"Year={year}, Day={day}")
        # print(header)
