import os
import time
from pathlib import Path

DAY = 6


class LanternFish:
    def __init__(self, timer, fish_list):
        self.timer = timer
        self.fish_list = fish_list

    def day_passes(self):
        if self.timer == 0:
            self.reproduce()
            self.timer = 6
        else:
            self.timer -= 1

    def reproduce(self):
        offspring = LanternFish(8, self.fish_list)
        self.fish_list.append(offspring)


def populate_fish_list(timers):
    fish_list = []
    for timer in timers:
        fish = LanternFish(timer, fish_list)
        fish_list.append(fish)
    return fish_list


def direct_method(timers, days_to_pass=256):
    """Iterate through a list of lanternfish and reproduce when a timer hits zero.
    This method becomes very slow as the list of fish grows long."""
    fish_list = populate_fish_list(timers)
    for day in range(days_to_pass):
        for fish in fish_list[:]:
            fish.day_passes()
        if (day % 16) == 0:
            print(f"Day {day:2}...")
    return len(fish_list)


def count_timers(timers):
    timer_counts = {n: 0 for n in range(9)}
    for n in timers:
        timer_counts[n] += 1
    return timer_counts


def faster_method(timers, days_to_pass):
    """Track the number of fish with a given number of days remaining on their
    internal timers. This vastly reduces the number of computations each day
    as the number of fish grows large."""
    animate = True
    timer_counts = count_timers(timers)
    for day in range(days_to_pass):
        new_counts = {n: 0 for n in range(9)}
        for i in range(9):
            if i == 0:
                new_counts[6] += timer_counts[0]
                new_counts[8] += timer_counts[0]
            else:
                new_counts[i - 1] += timer_counts[i]
        timer_counts = new_counts
        if animate:
            os.system("clear")
            print(f"After {day + 1} days...")
            for key in timer_counts.keys():
                print(f"Reproducing in {key} days: {timer_counts[key]}")
            time.sleep(0.1)

    number_of_fish = sum(timer_counts.values())
    return number_of_fish


def main():
    input_file = Path(__file__).parent / "input.txt"
    text = input_file.read_text()
    timers = [int(n) for n in text.split(",")]
    number_of_fish = faster_method(timers, days_to_pass=256)
    print(f"Number of fish: {number_of_fish}")


if __name__ == "__main__":
    main()
