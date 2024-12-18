from pathlib import Path
import heapq


data = (Path(__file__).parent.parent / "data/day17.txt").read_text().strip()


class HaltMachine(Exception):
    pass


class Machine:
    def __init__(self, data):
        self.parse(data)
        self._registers = self.registers
        self._program = self.program
        self.idx = 0
        self.output = []

    def parse(self, data):
        register_string, programs = data.split("\n\n")
        self.registers = []
        for reg in register_string.splitlines():
            self.registers.append(int(reg.split(":")[1]))
        self.program = list(map(int, programs.split(":")[1].split(',')))

    def combo(self):
        n = self.get(self.idx + 1)
        if 0 <= n <= 3:
            return n
        elif 4 <= n <= 6:
            idx = n - 4
            return self.registers[idx]
        assert False

    def dv(self, register):
        numerator = self.registers[0]
        den = 2 ** self.combo()
        self.registers[register] = numerator // den
        self.idx += 2

    def get(self, idx):
        if idx < 0 or self.idx >= len(self.program):
            raise HaltMachine()
        return self.program[idx]

    def literal(self):
        return self.get(self.idx + 1)

    def do_instruction(self):
        match self.get(self.idx):
            case 0:
                self.dv(0)
            case 1:
                ret = self.literal() ^ self.registers[1]
                self.registers[1] = ret
                self.idx += 2
            case 2:
                self.registers[1] = self.combo() % 8
                self.idx += 2
            case 3:
                a = self.registers[0]
                if a == 0:
                    self.idx += 2
                else:
                    self.idx = self.literal()
            case 4:
                b = self.registers[1]
                c = self.registers[2]
                self.registers[1] = b ^ c
                self.idx += 2
            case 5:
                ret = self.combo() % 8
                self.output.append(ret)
                self.idx += 2
                return self.output
            case 6:
                self.dv(1)
            case 7:
                self.dv(2)

    def reset(self):
        self.program = self._program
        self.output = []
        self.registers = self._registers
        self.idx = 0

    def check(self, output):
        if len(output) > len(self.program):
            return False
        return self.program[:len(output)] == output

    def run_at(self, a_register):
        self.reset()
        self.registers[0] = a_register
        return self.run()

    def binary_middle(self, low, high):
        return low + ((high - low) // 2) - 1

    def find_first_n_digit(self, n):
        initial = 1
        while True:
            self.run_at(initial)
            initial *= 2
            if len(self.output) >= n:
                break
        high = initial
        low = high // 2
        initial = self.binary_middle(low, high)
        while True:
            if high == low:
                return high
            self.run_at(initial)
            if len(self.output) == n:
                self.run_at(initial - 1)
                # if one previous gives us a shorter length, we found the correct initial value
                if len(self.output) == n - 1:
                    return initial
                else:
                    # otherwise, we're still too high
                    high = initial
                    initial = self.binary_middle(low, high)
            else:
                # we're too low
                low = initial
                initial = self.binary_middle(low, high)

    def run(self):
        while True:
            try:
                self.do_instruction()
            except HaltMachine:
                return self.output


machine = Machine(data)
print(machine.run())
machine.reset()
# output = machine.run()



print(machine.find_first_n_digit(len(machine.program) - 1))
print(machine.output)
#
# low = 35184372088832
# high = 281474976710655

indexes = [1] + [machine.find_first_n_digit(i) for i in range(2, len(machine.program) + 1)]

# machine.run_at(low + 4398046511104)
# machine.run_at(low + 4398046511103)
#     indexes[-1]*7
#     + indexes[-2]*2
#     + indexes[-3]*2
#     + indexes[-4]*6
#     + indexes[-5]*4
#     + indexes[-6]*2
#     + indexes[-7]*4
#     + indexes[-8]*5
#     + indexes[-9]*5
# ))


def compute(coeffs):
    return sum(c * indexes[-(i + 1)] for i, c in enumerate(coeffs))

def search(m: Machine):
    stack = [[x] for x in range(8)]
    while stack:
        coeffs = heapq.heappop(stack)
        a = compute(coeffs)
        idx = len(coeffs)
        m.run_at(a)
        if m.output == m.program:
            return a
        if m.program[-idx] == m.output[-idx]:
            for i in range(8):
                heapq.heappush(stack, coeffs + [i])


p2 = search(machine)
print(f"{p2=}")
