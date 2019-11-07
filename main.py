import sys
import memory as mem_class
from prog_exec import prog_run


def main():
    # Check system inputs and run correct commands
    if len(sys.argv) > 2:
        print("Usage: python3.7", sys.argv[0], "[file.o]\n")
        sys.exit(0)

    # Allocate emulator memory
    e_mem = mem_class.Memory(65536)

    # Check if file was given. If so, parse it into memory
    if len(sys.argv) == 2:
        parse_file(e_mem)

    # Evaluate User input
    while 1:
        user_in = input('> ')
        evaluate(e_mem, user_in)


def evaluate(e_mem, user_in):
    user_in = user_in.split(' ')
    for i in range(len(user_in)):
        if user_in[i] == "exit":
            scream_and_die()
        elif 'R' in user_in[i]:
            prog_run(user_in[i])
        elif ':' in user_in[i]:
            if "exit" in user_in:
                scream_and_die()
            edit_mem(e_mem, user_in[i:])
            break
        elif '.' in user_in[i]:
            print_range(e_mem, user_in[i])
        elif user_in[i] == '':
            pass
        else:
            print_one(e_mem, user_in[i])


def print_one(e_mem, user_in):
    user_in = user_in.split(' ')
    addr_in = int(user_in[0], 16)
    print(user_in[0], ' ', '{:02X}'.format(e_mem.memory[addr_in]))


def print_range(e_mem, user_in):
    user_in = user_in.split('.')
    if len(user_in) == 2:
        addr_in = (int(user_in[0], 16), int(user_in[1], 16))
        pos = 0
        for i in range(addr_in[0], addr_in[1] + 1):
            if (pos % 8) == 0:
                print('{:02X}'.format(i), ' ', '{:02X}'.format(e_mem.memory[i]), end=' ')
            elif (pos % 8) == 7:
                print('{:02X}'.format(e_mem.memory[i]))
            else:
                print('{:02X}'.format(e_mem.memory[i]), end=' ')
            pos += 1
        if (pos % 8) != 0:
            print()


def edit_mem(e_mem, user_in):
    if len(user_in) > 1:
        addr_in = user_in[0][0:-1]  # Puts address in readable format
        curr_addr = int(addr_in, 16)
        pos = 1
        for i in range(curr_addr, curr_addr + len(user_in) - 1):
            e_mem.memory[i] = int(user_in[pos], 16)
            pos += 1


def parse_file(e_mem):
    # Open and parse file
    try:  # Attempt to open file
        file_in = open(sys.argv[1], "r")
    except IOError:  # Could not find file
        print("Could not find \"", sys.argv[1], "\". Please try again.")
        sys.exit(1)
    except:  # Unknown error
        print("An unknown error has occurred while reading file. Please try again.")
        sys.exit(1)

    # Read in file as string
    string_in = file_in.read()
    string_in = string_in.replace("\n", "")

    # Parse string
    segments = string_in.split(":")
    for i in segments:
        if len(i) != 0:
            if i[7] != 1:
                addr = i[2:6]
                addr = int(addr, 16)
                data = i[8:-2]
                for j in range(0, len(data), 2):
                    e_mem.memory[addr] = int(data[j:j+2], 16)  # Store as string
                    addr += 1


def scream_and_die():
    print("Emulator Shutting Down...", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()