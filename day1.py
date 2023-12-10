def get_carry_sums(calories):
    return list(
        sum(map(int, carry.split("x")))
        for carry
        in "x".join(calories).split("xx")
    )

with open("day1_input.txt") as f:
    calories = [line.strip() for line in f.readlines()]

    # part 1
    print(max(get_carry_sums(calories)))

    # part 2
    print(sum(sorted(get_carry_sums(calories))[-3:]))

