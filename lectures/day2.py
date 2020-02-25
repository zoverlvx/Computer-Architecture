import sys

PRINT_BEEJ      = 1
HALT            = 2
PRINT_NUM       = 3
SAVE            = 4 # saves a value to the register
PRINT_REGISTER  = 5 # prints the value in a register
ADD             = 6 # adds 2 registers, stores result in 1st reg

# 256 bytes of memory
memory = [0] * 256

# 8 bit register
register = [0] * 8

# program counter
pc = 0

def load_memory(filename):
    try:
        address = 0
        # open the file
        with open(filename) as f:
            # read all the lines
            for line in f:
                # parse out comments
                comment_split = line.strip().split("#")
                
                # strips additional space from text
                value = comment_split[0].strip()

                if value == "":
                    continue

                # converts the "numbers" from str to int
                num = int(value)
                memory[address] = num
                address += 1
    
    except FileNotFoundError:
        print("File not found.")
        sys.exit(2)

if len(sys.argv) != 2:
    print("ERROR: Must have file name")
    sys.exit(1)

load_memory(sys.argv[1])

print(memory)

while True:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == SAVE:
        # save a value to a register
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        # print the value in a register
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2
    elif command == ADD:
        # add two registers, store the result in the first reg
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    elif command == HALT:
        sys.exit(0)
    else:
        print(F"Command invalid: {command}")
        sys.exit(1)
