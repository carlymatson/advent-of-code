import os
import pathlib
import re
import time

from grid import Grid
from utils import ansify

DAY = 4


def get_input(use_example=False):
    input_file = pathlib.Path(__file__).parent / "input.txt"
    text = input_file.read_text()
    boards = text.split("\n\n")
    ball_list = boards.pop(0).split(",")
    ball_list = [int(ball) for ball in ball_list]
    bingo_cards = [Bingo(board) for board in boards]
    return ball_list, bingo_cards


class Bingo(Grid):
    ROWS = [[(i, j) for i in range(5)] for j in range(5)]
    COLS = [[(i, j) for j in range(5)] for i in range(5)]
    DIAGS = [[(i, i) for i in range(5)], [(i, 4 - i) for i in range(5)]]

    def __init__(self, grid):
        parser = lambda row: [int(n) for n in re.findall("\d+", row)]
        grid = Grid.from_string(grid, row_parser=parser)
        super().__init__(grid)
        self.tokens = [[False for i in range(5)] for j in range(5)]

    def mark_off(self, ball):
        for row in range(5):
            for col in range(5):
                if self.grid[row][col] == ball:
                    self.tokens[row][col] = True
                    return

    def check_line(self, line):
        has_tokens = [self.tokens[y][x] for (x, y) in line]
        return all(has_tokens)

    def is_winner(self):
        lines = Bingo.ROWS + Bingo.COLS  # + Bingo.DIAGS
        for line in lines:
            if self.check_line(line):
                return True
        return False

    def score(self):
        total = 0
        for i in range(5):
            for j in range(5):
                if not self.tokens[i][j]:
                    total += self.grid[i][j]
        return total

    def style_tokens(num, has_token):
        code = "33"
        num_string = f"{num:2}"
        result = ansify(num_string, code) if has_token else num_string
        return result

    def show_board(self):
        for i in range(5):
            row = self.grid[i]
            tokens = self.tokens[i]
            row = map(Bingo.style_tokens, row, tokens)
            print(" ".join(row))


def get_next_winner(balls, cards):
    animate = False
    for ball in balls:
        for i, card in enumerate(cards[:]):
            card.mark_off(ball)
            if card.is_winner():
                cards.remove(card)
                yield card, ball
            if animate:
                if i == 0:
                    time.sleep(0.5)
                    os.system("clear")
                    print(f"Rolling... {ball}")
                    card.show_board()


def main():
    ball_list, bingo_cards = get_input(use_example=False)
    winner_generator = get_next_winner(ball_list, bingo_cards)

    # Get first winner.
    first_winner, first_ball = next(winner_generator)

    # Continue through all other cards to get to last winner.
    for winner, ball in winner_generator:
        last_winner, last_ball = winner, ball

    # Compute scores and display results.
    first_score = first_winner.score()
    last_score = last_winner.score()

    first_winner.show_board()
    print("-" * 15)
    last_winner.show_board()
    print(f"First winner: {first_score} * {first_ball} = {first_score * first_ball}")
    print(f"Last winner: {last_score} * {last_ball} = {last_score * last_ball}")


if __name__ == "__main__":
    main()
