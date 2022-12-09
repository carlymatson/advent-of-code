from typing import Tuple, List, Any, Callable, Union
from pprint import pprint

Point2D = Tuple[int, int]
IntSlice = Union[int, slice]


class Array2D:
    def __init__(
        self,
        arr,
        row_sep: str = "\n",
        col_sep: str = "",
        stringify: Callable[[int, int, Any], str] = lambda x, y, item: str(item),
    ):
        self.array = arr
        self.row_sep = row_sep
        self.col_sep = col_sep
        self.stringify = stringify

    @classmethod
    def from_string(
        cls,
        s: str,
        row_sep: str = "\n",
        col_sep: str = "",
        stringify: Callable[[int, int, Any], str] = lambda x, y, item: str(item),
        parser: Callable = lambda x: x,
    ):
        split_row = lambda row: row.split(col_sep) if col_sep else list(row)
        array = [[parser(x) for x in split_row(row)] for row in s.split(row_sep)]
        return cls(array, row_sep=row_sep, col_sep=col_sep, stringify=stringify)

    def __getitem__(self, tup: Tuple[IntSlice, IntSlice]):
        x, y = tup
        if isinstance(y, slice):
            retval = [row[x] for row in self.array[y]]
        else:
            retval = self.array[y][x]
        return retval

    def __str__(self) -> str:
        cells = [
            [self.stringify(x, y, item) for x, item in enumerate(row)]
            for y, row in enumerate(self.array)
        ]
        return self.row_sep.join([self.col_sep.join(row) for row in cells])

    def size(self) -> Point2D:
        a = self.array
        return len(a[0]), len(a)

    def transpose(self) -> "Array2D":
        width, height = self.size()
        trans = [[self[x, y] for y in range(height)] for x in range(width)]
        return Array2D(trans)

    def enumerate(self) -> List[Tuple[Point2D, Any]]:
        return [
            ((x, y), item)
            for y, row in enumerate(self.array)
            for x, item in enumerate(row)
        ]
