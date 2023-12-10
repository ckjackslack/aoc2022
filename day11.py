import re
import time
from collections import Counter, deque, namedtuple
from dataclasses import dataclass
from operator import mul
from typing import List, Callable, Deque
from pprint import pp

# import rust
from numba import njit, jit
from gmpy2 import mpz, mul as _mul, add as _add

from lib import multiply


@dataclass
class Monkey:
  number: int
  items: Deque[int]
  operation: Callable[[int], int]
  test: Callable[[int], bool]

current_monkey_data = {}

LineParser = namedtuple("LineParser", "what parse key")

def save_into(self, value):
  global current_monkey_data
  current_monkey_data[self.key] = value

setattr(LineParser, "save_into", save_into)

get_int = lambda s: int("".join(c for c in s if c.isdigit()))
get_arr = lambda s: deque(map(int, re.search(r'(\d.*?$)', s).group(0).split(", ")))
get_expr = lambda s: s[s.find("=") + 2:]

parsers = [
  LineParser("Monkey", get_int, "number"),
  LineParser("Starting", get_arr, "items"),
  LineParser("Operation", get_expr, "operation"),
  LineParser("Test", get_int, "test"),
  LineParser("If true",  get_int, "cond_true"),
  LineParser("If false", get_int, "cond_false"),
]


def get_monkeys(filename, optimize=None):
  global current_monkey_data
  monkeys = []
  with open(filename) as f:
    for line in f:
      line = line.strip()

      if not line:
        continue

      for parser in parsers:
        if line.startswith(parser.what):
          out = parser.parse(line)
          parser.save_into(out)

      if len(current_monkey_data) == 6:
        test = current_monkey_data.pop("test")
        nfalse = current_monkey_data.pop("cond_false")
        ntrue = current_monkey_data.pop("cond_true")
        # print(test, ntrue, nfalse)
        code = "lambda n: {} if n % {} == 0 else {}".format(ntrue, test, nfalse)
        # print(code)
        current_monkey_data["test"] = eval(code)

        op = current_monkey_data.pop("operation")
        # print(op)
        # optimize = "rust"
        # optimize = "gmpy2"
        # optimize = "custom"

        if optimize:
          operand1, operator, operand2 = op.split()
          if optimize == "rust":
            if operand1.isdigit():
              operand1 = f'"{operand1}"'
            if operand2.isdigit():
              operand2 = f'"{operand2}"'

            # r_wrapper_m = "amultiply"
            r_wrapper_m = "multiplybig"
            r_wrapper_a = "aadd"
            if operator == "*":
              op = f"rust.{r_wrapper_m}({operand1}, {operand2})"
            elif operator == "+":
              op = f"rust.{r_wrapper_a}({operand1}, {operand2})"
          elif optimize == "gmpy2":
            wrapper = "mpz"
            if not operand1.isdigit():
              operand1 = f"{wrapper}({operand1})"
            if not operand2.isdigit():
              operand2 = f"{wrapper}({operand2})"
            op = f"{operand1} {operator} {operand2}"
          elif optimize == "custom":
            if operator == "*":
              op = f"multiply({operand1}, {operand2})"

        code = "lambda old: {}".format(op)
        # print(code)
        optimized_fn = None
        # optimized_fn = lambda fn: njit(fn)
        # optimized_fn = lambda fn: jit('void(uint64)', forceobj=True)(fn)
        if callable(optimized_fn):
          current_monkey_data["operation"] = optimized_fn(eval(code))
        else:
          current_monkey_data["operation"] = eval(code)

        monkeys.append(Monkey(**current_monkey_data))

        current_monkey_data = {}

  return monkeys


def part_one(monkeys, number_of_rounds=20, do_division=True):
  monkeys = monkeys.copy()
  no_of_inspections = Counter()
  max_so_far = 0
  for cur_round in range(number_of_rounds):
    for monkey in monkeys:
      while len(monkey.items) > 0:
        item = monkey.items.popleft()
        if item > max_so_far:
          max_so_far = item
        # item = str(item)
        # try:
        worry_level = monkey.operation(item)
        # print(worry_level)
        # except:
          # print(cur_round)
          # print(item)
          # exit()
        if do_division:
          worry_level //= 3
        # worry_level = int(worry_level)
        monkey_no = monkey.test(worry_level)
        # print(f"Giving item with worry level {worry_level} to monkey#{monkey_no}")
        target_monkey = monkeys[monkey_no]
        target_monkey.items.append(worry_level)
        no_of_inspections.update({monkey.number: 1})
    # print(f"After round {cur_round + 1}:")
    # pp([
    #   f"Monkey {m.number}: {', '.join(map(str, m.items))}"
    #   for m
    #   in monkeys
    # ], width=100)
    # break
  print(no_of_inspections)
  # print(max_so_far, len(str(max_so_far)))
  return mul(*(v for k, v in no_of_inspections.most_common(2)))


def part_two(monkeys):
  return part_one(monkeys, number_of_rounds=500, do_division=False)


def main():
  start = time.time()
  # filename = "day11_input.txt"
  filename = "day11_example.txt"
  monkeys = get_monkeys(filename)
  # pp(monkeys)
  # print(part_one(monkeys))

  # 2714213144 -> too low

  # after 1000 -> Counter({0: 5204, 1: 4792, 2: 199, 3: 5192})
  print(part_two(monkeys))

  print(f"Took {time.time()-start:.6f} seconds.")

  # using gmpy:
  # 900 ~ 10s
  # 1000 ~ 42s

if __name__ == '__main__':
  main()

# U1024
# 105894149134020442058971073880890933280925737489593093749132577188036203284185569301861872817679342597770017527618152998521810937638590629863332882642450310286658400932993

# U2048
# 152167936456310830400675797428164272026108067799285826732741344612032360939435158085120665436660830978683003050938770557011612884803859490442402242030319675771440550089058021740413545738417731143773933863890173373368167496607723911136194455320079310852591631133096499380875286403022752125602968184502195451871617055910552996785476294643023868770843257815460231154677709

# U4096
# 314213994195733205444576529337714482235022349905721137702295756051771266073144765669559731962099823682940731687893197958355267143292166964124468506103162596985602178874131966928320985087954054488709675755277072828801388196224409736137389122165552029746761849580568793562850818849815018746759506522748620629481828426947011287758621856977184605120345153641785185325645946901564924763612710229681771513356406570671778800179156732576996450303969310551588475226093887962331380794643211811530327067015238285824204044072277646619489033049562392019901548418906670428799167932567223976522817367191772280952380886372540921521743264493836421644984037992036407618492256684162387962591460828488975947605914397949300907232944384423760592002548871159402917096180046894483585307061

# https://docs.rs/num-bigint/latest/num_bigint/struct.BigUint.html
# https://lib.rs/crates/rug
# https://doc.rust-lang.org/rust-by-example/conversion/string.html
# https://betterprogramming.pub/strings-in-rust-28c08a2d3130
# https://docs.rs/rug/latest/rug/
# https://doc.rust-lang.org/book/ch03-02-data-types.html
# https://doc.rust-lang.org/std/primitive.u128.html
# https://github.com/saidvandeklundert/pyo3/blob/main/multiply/multiply.py
# http://saidvandeklundert.net/learn/2021-11-18-calling-rust-from-python-using-pyo3/

