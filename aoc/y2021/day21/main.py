def roll_die():
    roll = 1
    while True:
        yield roll
        roll += 1


class Player:
    def __init__(self, starting_space, die_roll):
        self.space = starting_space
        self.score = 0
        self.roll_die = die_roll

    def move(self, num_spaces):
        self.space += num_spaces % 10
        if self.space > 10:
            self.space -= 10

    def take_turn(self):
        for _ in range(3):
            roll = next(self.roll_die)
            self.move(roll)
        self.score += self.space

    def __repr__(self):
        return f"P(x={self.space},score={self.score})"


def main():
    die = roll_die()
    p1 = Player(starting_space=7, roll_die=die)
    p2 = Player(starting_space=6, roll_die=die)
    turns = 0
    while True:
        turns += 1
        p1.take_turn()
        if p1.score >= 1000:
            losing_score = p2.score
            break
        p2.take_turn()
        if p2.score >= 1000:
            losing_score = p1.score
            break
    print(p1, p2)
    next_roll = next(die)
    answer = losing_score * (next_roll - 1)
    print(f"Score: {next_roll-1} * {losing_score} = {answer}")


if __name__ == "__main__":
    main()
