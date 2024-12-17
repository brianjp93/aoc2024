from pathlib import Path


data = (Path(__file__).parent.parent / "data/day17.txt").read_text().strip()

# data = """Register A: 729
# Register B: 0
# Register C: 0
#
# Program: 0,1,5,4,3,0"""

# data = """Register A: 10
# Register B: 0
# Register C: 0
#
# Program: 5,0,5,1,5,4"""

# data = """Register A: 2024
# Register B: 0
# Register C: 0
#
# Program: 0,3,5,4,3,0"""


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
            # print(f"Getting combo at index {idx}")
            return self.registers[idx]
        assert False

    def dv(self, register):
        # print(f"running division on register {register}")
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
        # print(f"looking at {self.idx=}, {self.get(self.idx)=}")
        match self.get(self.idx):
            case 0:
                # print('running 0')
                self.dv(0)
            case 1:
                # print('running 1')
                ret = self.literal() ^ self.registers[1]
                self.registers[1] = ret
                self.idx += 2
            case 2:
                # print('running 2')
                self.registers[1] = self.combo() % 8
                self.idx += 2
            case 3:
                # print('running 3')
                a = self.registers[0]
                if a == 0:
                    self.idx += 2
                else:
                    self.idx = self.literal()
            case 4:
                # print('running 4')
                b = self.registers[1]
                c = self.registers[2]
                self.registers[1] = b ^ c
                self.idx += 2
            case 5:
                # print('running 5')
                ret = self.combo() % 8
                # print(f'Got mod 8 value {ret}')
                self.output.append(ret)
                self.idx += 2
                return self.output
            case 6:
                # print('running 6')
                self.dv(1)
            case 7:
                # print('running 7')
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

    def find_dumb(self):
        initial = 3889057078656
        while True:
            self.reset()
            self.registers[0] = initial
            self.run()
            print(initial)
            print(self.output)
            if self.output == self.program:
                return initial
            initial += 100000

    def find(self):
        initial = 2799023321088
        found_high = False
        high = float('inf')
        low = 0
        program = int(''.join(map(str, reversed(self.program))))
        while True:
            print(f"checking A={initial}")
            self.reset()
            self.registers[0] = initial
            while True:
                try:
                    self.do_instruction()
                except HaltMachine:
                    break

            print(f"{initial=}")
            print(self.output)

            output = int(''.join(map(str, reversed(self.output))))
            if found_high:
                print(f" {output=}")
                print(f"{initial=}")
                print(f"{low=}, {high=}")
                if output < program:
                    print('too high')
                    high = initial
                    initial = low + ((high - low) // 2)
                elif output > program:
                    print('too low')
                    low = initial
                    initial = low + ((high - low) // 2)
                else:
                    return initial
                input()
            else:
                if output > program:
                    input()
                    found_high = True
                    high = initial
                    low = high // 2
                    initial = low + ((high - low) // 2)
                else:
                    initial = initial * 2

    def run(self):
        while True:
            try:
                self.do_instruction()
            except HaltMachine:
                return self.output


machine = Machine(data)
print(machine.run())
machine.reset()
# print(machine.program, machine.registers)
# output = machine.run()
# print(','.join(map(str,output)))

# print(machine.find())
print(machine.find_dumb())
