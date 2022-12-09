import pytest

import y2022


@pytest.mark.parametrize(
    "solution_module, answer1, answer2",
    [
        (y2022.day_01, 69693, 200945),
        (y2022.day_02, 13221, 13131),
        (y2022.day_03, 7821, 2752),
        (y2022.day_04, 456, 808),
        (y2022.day_05, "TDCHVHJTG", "NGCMPJLHV"),
        (y2022.day_06, 1093, 3534),
        (y2022.day_07, 1845346, 3636703),
        (y2022.day_08, 1854, 527340),
        (y2022.day_09, 6090, 2566),
    ],
)
def test_solutions(solution_module, answer1, answer2):
    part_1_answer, part_2_answer = solution_module.main.solution()
    assert (part_1_answer, part_2_answer) == (answer1, answer2)
