from pathlib import Path

from packet import BitReader, Packet

HEX_DIGITS = "0123456789ABCDEF"


def load_input(use_example: bool):
    filename = "example.txt" if use_example else "input.txt"
    file_path = Path(__file__).parent / filename
    text = file_path.read_text()
    with open(filename, "r") as f:
        text = f.read()
    return text


def hex_to_binary(hex):
    h = [bit for digit in hex for bit in int_to_binary(HEX_DIGITS.index(digit))]
    return h


def int_to_binary(n, num_places=4):
    s = []
    for place in range(num_places):
        digit = n % 2
        s.append(digit)
        n = int((n - digit) / 2)
    return list(reversed(s))


def binary_to_int(bits):
    n = 0
    for digit in bits:
        n *= 2
        n += digit
    return n


def get_literal(bit_reader):
    bits = []
    is_not_last = True
    while is_not_last:
        next_bit = next(bit_reader.read(1))
        is_not_last = bool(next_bit)
        chunk = list(bit_reader.read(4))
        bits = bits + chunk
    return binary_to_int(bits)


def get_subpackets(bit_reader, length_type_id):
    subpackets = []
    num_to_read = binary_to_int(bit_reader.read(11 if length_type_id else 15))
    while num_to_read > 0:
        packet, bits_read = parse_packet(bit_reader)
        subpackets.append(packet)
        num_read = 1 if length_type_id else bits_read
        num_to_read -= num_read
    return subpackets


def parse_packet(bit_reader):
    bits_0 = bit_reader.bits_read
    version = binary_to_int(bit_reader.read(3))
    type_id = binary_to_int(bit_reader.read(3))
    if type_id == 4:
        params = {"literal": get_literal(bit_reader)}
    else:
        length_type_id = next(bit_reader.read(1))
        params = {
            "length_type_id": length_type_id,
            "subpackets": get_subpackets(bit_reader, length_type_id),
        }
    bits_read = bit_reader.bits_read - bits_0
    return Packet(version, type_id, params), bits_read


def main():
    text = load_input(True)
    hex = hex_to_binary(text)
    binary_stream = (b for b in hex)
    bit_reader = BitReader(binary_stream)
    packet, _ = parse_packet(bit_reader)
    print(f"Version total: {packet.get_version_total()}")
    print(f"Evaluation: {packet.evaluate(True)}")


if __name__ == "__main__":
    main()
