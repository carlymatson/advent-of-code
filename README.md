# Advent of Code

This project contains my solutions for the Advent of Code challenge problems 
from 2019, 2020, 2021, and 2022. All solutions are written using python 3.8.
## Solutions

 - [2019 solutions](y2019/y2019.md)

 - [2020 solutions](y2020/y2020.md)

 - [2021 solutions](y2021/y2021.md)

 - [2022 solutions](y2022/y2022.md)

## How to Use
 Run the solution for any given date by running
 ```
 python3 solve.py <year> <date>
 ```
 Most of the solutions can be run without any third party libraries, but for full functionality use the following commands to create and activate a virtual environment and install the needed libraries.
 ```
 python3 -m venv .venv
 source .venv/bin/activate
 python3 -m pip install --upgrade pip
 python3 -m pip install -r requirements.txt
 ```

 To see which days have solutions using [pytest](https://docs.pytest.org/en/7.2.x/), run
 ```
 python3 -m pytest tests --tb=no
 ```
