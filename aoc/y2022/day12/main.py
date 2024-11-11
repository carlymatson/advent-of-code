# import re
# from pathlib import Path
# from typing import Tuple, List, Dict, Set
# from pprint import pprint
# from pyadvent.array_2d import Array2D

# # from pyadvent.geometry import Point
# from pyadvent import geometry as geom
# from pyadvent.maze import MazeSolver, Walk

# ### Model ###

# Point2D = Tuple[int, int]


# class Map(Array2D):
#     def __init__(self, arr, start, goal):
#         super().__init__(arr=arr, col_sep=",")
#         self.start = start  # Point
#         self.goal = goal  # Point

#     def from_text(s: str) -> "Map":
#         rows = [[c for c in row] for row in s.split("\n")]
#         start = (0, 0)
#         end = (0, 0)
#         for y, row in enumerate(rows):
#             for x, c in enumerate(row):
#                 if c == "S":
#                     start = (x, y)
#                     row[x] = "a"
#                 if c == "E":
#                     end = (x, y)
#                     row[x] = "z"
#         elevations = [[ord(c) - ord("a") for c in row] for row in rows]
#         return Map(elevations, start, end)

#     def get_neighbors(self, node: Point2D) -> List[Tuple[Point2D, int]]:
#         opts = []
#         x, y = node
#         height = self[x, y]
#         for dir in geom.DIRECTIONS.values():
#             x2, y2 = geom.Point(*node) + dir
#             try:
#                 height2 = self[x2, y2]
#                 if height2 <= height + 1:
#                     opts.append(((x2, y2), 1))
#             except IndexError:
#                 continue
#         return opts


# ### Parse Input ###


# def load_input() -> str:
#     filepath = Path(__file__).parent / "input.txt"
#     text = filepath.read_text().strip()
#     arr = Map.from_text(text)
#     return arr


# ### Solution ###


# def solution() -> Tuple[int, int]:
#     map = load_input()

#     ### Part 1 ###
#     frontier = [Walk(nodes=[map.start], length=0)]
#     solver = MazeSolver(maze=map, frontier=frontier)
#     solver.explore_all()
#     best_route = solver.best_known_route[map.goal]
#     part_1_solution = best_route.length

#     ### Part 2 ###
#     lowest_points = set()
#     for point, height in map.enumerate():
#         if height == 0:
#             lowest_points.add(point)
#     frontier = [Walk(nodes=[n], length=0) for n in lowest_points]
#     solver = MazeSolver(maze=map, frontier=frontier)
#     solver.explore_all()
#     best_route = solver.best_known_route[map.goal]
#     part_2_solution = best_route.length

#     return part_1_solution, part_2_solution
