import sys
import memory as mem_class


def main():
    # Check system inputs and run correct commands
    if len(sys.argv) > 2:
        print("Usage: python3.7", sys.argv[0], "[file.o]\n")
        sys.exit(0)

    # Allocate emulator memory
    e_mem = mem_class.Memory(["00"] * 65536, 0, 0, 0, 0, 0, 255)

    # Check if file was given. If so, parse it into memory
    if len(sys.argv) == 2:
        parse(e_mem)

    # Get user input and evaluate
    user_in = input('> ')

    # Evaluate User input
    while user_in != "exit":
        screen(e_mem, user_in)
        user_in = input('> ')

    # Exit program
    print("Emulator Shutting Down...")


def screen(e_mem, user_in):
    # If R is at end, run
    if user_in[-1] == 'R':
        print("PC  OPC  INS   AMOD OPRND  AC  XR YR SP NV-BDIZC")
        print(user_in[0:-1])
    else:
        # If range then print range
        addr_in = user_in.split('.')
        if len(addr_in) == 2:
            addr_in[0] = int(addr_in[0], 16)
            addr_in[1] = int(addr_in[1], 16)
            pos = 0
            for i in range(addr_in[0], addr_in[1] + 1):
                if (pos % 8) == 0:
                    addr_hex = hex(i)
                    print(addr_hex[2:], ' ', e_mem.memory[i], end = ' ')
                elif (pos % 8) == 7:
                    print(e_mem.memory[i])
                else:
                    print(e_mem.memory[i], end = ' ')
                pos += 1
            if (pos % 8) != 0:
                print()

        # If address input then input
        else:
            addr_in = user_in.split(' ')
            if len(addr_in) > 1:
                addr_in[0] = addr_in[0][0:-1]  # Puts address in readable format
                curr_addr = int(addr_in[0], 16)
                pos = 1
                for i in range(curr_addr, curr_addr + len(addr_in) - 1):
                    e_mem.memory[i] = addr_in[pos]
                    pos += 1

            # If single address then output contents
            else:
                addr_in[0] = int(addr_in[0], 16)
                addr_hex = hex(addr_in[0])
                print(addr_hex[2:], " ", e_mem.memory[addr_in[0]])


def parse(e_mem):
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
                    e_mem.memory[addr] = data[j:j+2]  # Store as string
                    addr += 1


if __name__ == "__main__":
    main()