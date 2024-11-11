from pathlib import Path


class CaveSystem:
    def __init__(self, text):
        self.connections = {}
        lines = text.split("\n")
        for line in lines:
            cave1, cave2 = line.split("-")
            self.add_connection(cave1, cave2)

    def add_connection(self, cave1, cave2):
        if cave1 not in self.connections:
            self.connections[cave1] = []
        if cave2 not in self.connections:
            self.connections[cave2] = []
        self.connections[cave1].append(cave2)
        self.connections[cave2].append(cave1)

    def get_options(self, route):
        current_cave = route[-1]
        small_caves_visited = [cave for cave in route if str.islower(cave)]
        none_revisited_yet = len(set(small_caves_visited)) == len(small_caves_visited)
        allowable = (
            lambda cave: none_revisited_yet or str.isupper(cave) or cave not in route
        )
        connections = self.connections[current_cave]
        options = [cave for cave in connections if allowable(cave) and cave != "start"]
        return options


def main():
    input_file = Path(__file__).parent / "input.txt"
    text = input_file.read_text()
    cave_sys = CaveSystem(text)
    unfinished_routes = [["start"]]
    finished_routes = []
    while len(unfinished_routes) > 0:
        rte = unfinished_routes.pop()
        opts = cave_sys.get_options(rte)
        for opt in opts:
            new_route = rte + [opt]
            if opt == "end":
                finished_routes.append(new_route)
            else:
                unfinished_routes.append(new_route)
    print(len(finished_routes))


if __name__ == "__main__":
    main()
