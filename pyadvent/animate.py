import os
import time
from typing import Optional

TERMINAL_HEIGHT = 100
TERMINAL_WIDTH = 80


def clear_terminal():
    ansi_clear_code = "\033[1;1H"
    blank_rectangle = "\n".join([" " * TERMINAL_WIDTH for _ in range(TERMINAL_HEIGHT)])
    print(ansi_clear_code + blank_rectangle)


def progress_bar(percent: float) -> str:
    width = 100
    bar = "#" * int(percent) + "." * (width - int(percent))
    pic = f"[{bar}] {percent}%"
    return pic


def animate(
    screen: str,
    clear_screen: bool = True,
    await_user: bool = True,
    delay: Optional[float] = 0.5,
) -> None:
    if clear_screen:
        clear_terminal()
    else:
        horizontal_rule = "-" * TERMINAL_WIDTH
        print(horizontal_rule)
    print(screen)
    if await_user:
        input("(enter) ")
    elif delay is not None:
        time.sleep(delay)


if __name__ == "__main__":
    clear_terminal()
    TERMINAL_WIDTH = 5
    for turn in range(100):
        pic = progress_bar(turn + 1)
        s = f"Turn {turn}\n" + pic
        animate(s, clear_screen=True, delay=None)
