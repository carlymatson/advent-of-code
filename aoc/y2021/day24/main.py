import re
from collections import defaultdict, namedtuple
from pathlib import Path
from pprint import pprint


def load_input(example=None):
    file = "input.txt" if example is None else f"example{example}.txt"
    path = Path(__file__).parent / file
    return path.read_text()


class ALU:
    def __init__(self, inputs=None, registers=None, code=None):
        self.registers = (
            registers if registers is not None else {reg: 0 for reg in "wxyz"}
        )
        self.inputs = inputs if inputs is not None else []
        self.code = code if code is not None else []
        self.handlers = {
            "inp": self.inp,
            "add": self.add,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "eql": self.eql,
        }

    def copy(self):
        return ALU(
            inputs=list(self.inputs),
            registers=dict(self.registers),
            code=list(self.code),
        )

    def handle_instruction(self, instruction):
        parts = instruction.split(" ")
        command, params = parts[0], parts[1:]
        if len(params) > 1:
            b = params[1]
            try:
                b = int(b)
                params[1] = b
            except ValueError as e:
                params[1] = self.registers[b]
        self.handlers[command](*params)

    def inp(self, a):
        input = self.inputs.pop(0)
        self.registers[a] = input

    def add(self, a, b):
        self.registers[a] += b

    def mul(self, a, b):
        self.registers[a] *= b

    def div(self, a, b):
        self.registers[a] = int(self.registers[a] / b)

    def mod(self, a, b):
        self.registers[a] %= b

    def eql(self, a, b):
        self.registers[a] = int(self.registers[a] == b)

    def run(self, instructions=None):
        if instructions:
            self.code.extend(instructions)
        while self.code:
            inst = self.code.pop(0)
            try:
                self.handle_instruction(inst)
            except IndexError as e:
                return False
        return True


def model_number_generator():
    model_no = int("9" * 14)
    while model_no > 10**13:
        if "0" not in list(str(model_no)):
            yield model_no
        model_no -= 1


seen = set()


def find_highest_model_no(alu, num_digits):
    global seen
    if len(seen) > 200:
        print(seen)
        return
    if num_digits == 4:
        print(f"Number seen: {len(seen)}")
        if len(seen) > 200:
            print(seen)
            return
        # print(".", end="", flush=True)
    state = tuple([alu.registers[r] for r in "wxyz"] + [num_digits])
    if state in seen:
        return None
    seen.add(state)
    if num_digits == 0:
        if alu.registers["z"] == 0:
            print(f"Valid! Registers: {alu.registers}")
            return ""
        else:
            return None
    for digit in range(9, 0, -1):
        new_alu = alu.copy()
        new_alu.inputs.append(digit)
        new_alu.run()
        highest = find_highest_model_no(new_alu, num_digits=num_digits - 1)
        if highest is not None:
            return str(digit) + highest
    return None


def main():
    code = load_input(example=None)

    pattern = """inp w
mul x 0
add x z
mod x 26
div z (\d+)
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (\d+)
mul y x
add z y"""
    snippets = re.findall(pattern, code)
    print(len(snippets))
    pprint(snippets)
    return

    instructions = code.split("\n")

    z_affecting = [inst for inst in instructions if inst[4] == "z"]
    pprint(z_affecting)
    z_affected = [inst for inst in instructions if len(inst) > 6 and inst[6] == "z"]
    pprint(z_affected)
    return
    turns = 0

    alu = ALU(code=instructions)
    model_no = find_highest_model_no(alu, 14)
    print(f"Highest model no: {model_no}")


if __name__ == "__main__":
    main()
