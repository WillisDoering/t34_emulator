import sys
import memory as mem_class


def main():
    # Check system inputs and run correct commands
    if len(sys.argv) > 2:
        print("Usage: python3.7", sys.argv[0], "[file.o]\n")
        sys.exit(0)

    # Allocate emulator memory
    e_mem = mem_class.Memory([0] * 65536, 0, 0, 0, 0, 0, 255)

    # Move on to display
    screen(e_mem)

    # Exit program
    print("Emulator Shutting Down...\n")


def screen(e_mem):
    # Check if file was given. If so, parse it into memory
    if len(sys.argv) == 2:
        parse(e_mem)


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
                addr = i[2:5]
                addr = int(addr, 16)
                data = i[8:-2]
                for j in range(0, len(data) + 2, 2):
                    e_mem.memory[addr] = data[j:j+2]  # Store as string
                    addr += 1


if __name__ == "__main__":
    main()