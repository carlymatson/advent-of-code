import json


class Snailfish:
    def __init__(self, entries):
        self.entries = entries

    @staticmethod
    def from_data(data):
        try:
            left, right = data
            return Snailfish.from_data(left) + Snailfish.from_data(right)
        except TypeError as e:
            entries = {"": data}
            return Snailfish(entries)

    @staticmethod
    def from_string(sf):
        data = json.loads(sf)
        return Snailfish.from_data(data)

    def __repr__(self):
        if "" in self.entries:
            return str(self.entries[""])
        left, right = self.get_children()
        return f"[{left},{right}]"

    def __add__(self, obj):
        left_entries = {"0" + k: v for k, v in self.entries.items()}
        right_entries = {"1" + k: v for k, v in obj.entries.items()}
        sum = Snailfish({**left_entries, **right_entries})
        return sum

    def get_children(self):
        left_entries = {k[1:]: v for k, v in self.entries.items() if k.startswith("0")}
        right_entries = {k[1:]: v for k, v in self.entries.items() if k.startswith("1")}
        if len(left_entries) == None:
            return None
        return Snailfish(left_entries), Snailfish(right_entries)

    def split(self, entry):
        value = self.entries[entry]
        half_rounded_down = int(value / 2)
        lkey, rkey = entry + "0", entry + "1"
        self.entries[lkey] = half_rounded_down
        self.entries[rkey] = value - half_rounded_down
        del self.entries[entry]
        return self

    def try_to_add(self, index, value):
        if 0 <= index and index < len(self.entries):
            key = sorted(self.entries.keys())[index]
            self.entries[key] += value

    def explode(self, entry):  # Make nicer?
        root = entry[:-1]
        sibling = root + "1"
        entries = self.entries
        index = sorted(entries.keys()).index(entry)
        lval, rval = entries[entry], entries[sibling]
        self.try_to_add(index - 1, lval)
        self.try_to_add(index + 2, rval)
        entries[root] = 0
        del entries[entry], entries[sibling]
        return self

    def perform_op(self, operation, key):
        func = self.explode if operation == "explode" else self.split
        return func(key)

    def first_reduction(self):
        entries = sorted(self.entries.items())
        for k, v in entries:
            if len(k) > 4:
                return "explode", k
        for k, v in entries:
            if v >= 10:
                return "split", k
        return None

    def reduce(self):
        next_reduction = self.first_reduction()
        while next_reduction is not None:
            operation, index = next_reduction
            self = self.perform_op(operation, index)
            next_reduction = self.first_reduction()
        return self

    def get_magnitude(self):
        if "" in self.entries:
            return self.entries[""]
        left, right = self.get_children()
        score = 3 * left.get_magnitude() + 2 * right.get_magnitude()
        return score
