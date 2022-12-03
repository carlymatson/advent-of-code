import pytest

import y2022


@pytest.mark.parametrize(
    "solution_module, answer1, answer2",
    [
        (y2022.day_01, 69693, 200945),
        (y2022.day_02, 13221, 13131),
        (y2022.day_03, 7821, 2752),
    ],
)
def test_solutions(solution_module, answer1, answer2):
    part_1_answer, part_2_answer = solution_module.main.solution()
    assert (part_1_answer, part_2_answer) == (answer1, answer2)
