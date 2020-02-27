"""CPU functionality."""

import sys

# setup constants for op codes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
SP = 7 # stack pointer R7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # creates 8 registers
        self.reg = [0] * 8

        # creates 256 bytes of memory
        self.ram = [0] * 256

        # creates a program counter (pc)
        self.pc = 0

    def ram_read(self, addr: int):
        return self.ram[addr]

    def write_ram(self, addr: int, value):
        self.ram[addr] = value

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        """
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        """

        try:
            address = 0

            # open file
            with open(file_name) as f:
                for line in f:
                    # strips out white space and
                    # splits at an inline comment
                    cleaned_line = line.strip().split("#")

                    # grabs the string number
                    value = cleaned_line[0].strip()

                    # checks if value is blank or not
                    # if so, skip to the next line
                    if value != "":
                        # convert number string to type int
                        # converts binary string to binary int
                        num = int(value, 2)
                        self.ram[address] = num
                        address += 1
                    else:
                        continue
        except FileNotFoundError:
            print("ERR: FILE NOT FOUND")
            sys.exit(2)

    def alu(self, op: str, reg_a: int, reg_b: int):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self, file_name):
        """Run the CPU."""

        # load the program into memory
        self.load(file_name)

        # read ram
        read_ram = self.ram_read

        # write ram
        write_ram = self.write_ram

        # run the program
        while True:
            
            pc = self.pc

            # queues operation to start at default
            # default is 0
            op = read_ram(pc)

            if op == LDI:
                self.reg[read_ram(pc + 1)] = read_ram(pc + 2)
                self.pc += 3
            elif op == PRN:
                print(self.reg[read_ram(pc + 1)])
                self.pc += 2
            elif op == MUL:
                # grab the ram values that hold the register indices
                reg_a = read_ram(pc + 1)
                reg_b = read_ram(pc + 2)
                # call on the ALU
                self.alu("MUL", reg_a, reg_b)
                # move program counter
                self.pc += 3
            elif op == PUSH:
                
                # decrement SP
                self.reg[SP] -= 1

                # get current mem address SP points to
                stack_addr = self.reg[SP]

                # grabs a reg number from the instruction
                reg_num = read_ram(pc + 1)

                # get the value out of the register
                val = self.reg[reg_num]

                # write the reg value to a position in the stack
                write_ram(stack_addr, val)
                self.pc += 2
            elif op == POP:
                # get the value out of memory
                stack_val = read_ram(self.reg[SP])

                # get the register number from the instruction in memory
                reg_num = read_ram(pc + 1)

                # set the value of a register to the value in the stack
                self.reg[reg_num] = stack_val

                # increment the SP
                self.reg[SP] += 1
                self.pc += 2
            elif op == HLT:
                sys.exit(1)
            else:
                print("ERR: UNKNOWN COMMAND:\t", op)

if len(sys.argv) == 2:
    file_name = sys.argv[1]

    cpu = CPU()

    # set the mem address the stack pointer is looking at

    cpu.reg[SP] = 0xf4
    cpu.run(file_name)
else:
    print("""
        ERR: PLEASE PROVIDE A FILE THAT YOU WISH TO RUN\n
        e.g. python cpu.py examples/FILE_NAME
    """)
    sys.exit(2)
