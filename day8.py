from functools import reduce
from operator import mul

prod = lambda arr: reduce(mul, arr, 1)

def main():
    filename = "day8_input.txt"
    # filename = "day8_example.txt"

    trees = []
    with open(filename) as f:
        for i, row in enumerate(f):
            tree_line = []
            for j, col in enumerate(row.strip()):
                tree_line.append(int(col))
            trees.append(tree_line)

    for tree_line in trees:
        print("".join(map(str, tree_line)))

    def part_one():
        rows, cols = len(trees), len(trees[0])
        visibile = 0

        for i in range(rows):
            for j in range(cols):
                if i in {0, rows - 1} or j in {0, cols - 1}:
                    visibile += 1
                    continue
                tree = trees[i][j]

                right = [tree > trees[i][j+x] for x in range(1, cols-j)]
                left = [tree > trees[i][j-x] for x in range(1, cols) if j-x >= 0]
                down = [tree > trees[i+x][j] for x in range(1, rows-i)]
                up = [tree > trees[i-x][j] for x in range(1, rows) if i-x >= 0]

                if any(map(all, [up, down, left, right])):
                    visibile += 1

        return visibile

    def part_two():
        rows, cols = len(trees), len(trees[0])
        highest_scenic_score = 0
        for i in range(rows):
            for j in range(cols):
                viewing_distance = []
                tree = trees[i][j]

                # up
                c = 0
                for x in range(1, rows):
                    if i - x < 0:
                        break
                    other = trees[i-x][j]
                    if x == 1 and tree == other:
                        c += 1
                        break
                    elif tree > other:
                        c += 1
                    else:
                        break
                if c > 0:
                    viewing_distance.append(c)

                # left
                c = 0
                for x in range(1, cols):
                    if j - x < 0:
                        break
                    other = trees[i][j-x]
                    if x == 1 and tree == other:
                        c += 1
                        break
                    elif tree > other:
                        c += 1
                    else:
                        break
                if c > 0:
                    viewing_distance.append(c)

                # right
                c = 0
                for x in range(1, cols-j):
                    other = trees[i][j+x]
                    if x == 1 and tree == other:
                        c += 1
                        break
                    elif tree > other:
                        c += 1
                    else:
                        break
                if c > 0:
                    viewing_distance.append(c)

                # down
                c = 0
                for x in range(1, rows-i):
                    other = trees[i+x][j]
                    if x == 1 and tree == other:
                        c += 1
                        break
                    elif tree > other:
                        c += 1
                    else:
                        break
                if c > 0:
                    viewing_distance.append(c)

                # print(viewing_distance)

                scenic_score = prod(viewing_distance)
                if scenic_score > highest_scenic_score:
                    print(viewing_distance)
                    highest_scenic_score = scenic_score

        return highest_scenic_score

    print(part_one())
    # print(part_two())

if __name__ == '__main__':
    main()