from collections import deque
from itertools import islice

def get_input():
    with open("day6_input.txt") as f:
        for line in f:
            for char in line:
                yield char


def is_marker(chars):
    return len(set(chars)) == len(chars)


def find_first_marker(packet_size):
    g = get_input()
    d = deque(islice(g, packet_size), maxlen=packet_size)
    value = packet_size
    while True:
        if is_marker(d):
            return value
        value += 1
        try:
            char = next(g)
            d.append(char)
        except StopIteration:
            break


def main():
    print(find_first_marker(4))
    print(find_first_marker(14))


if __name__ == '__main__':
    main()