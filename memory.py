# The class below holds the memory and registers for the emulator


# Status register (sr) is formatted with NV-BDIZC
class Memory:
    def __init__(self, mem_size):
        self.memory = bytearray(mem_size)   # Memory
        self.pc = 0     # pc: 16 bit (can be 24 bit but will implement error check on that later)
        self.registers = bytearray(5)       # All 5 registers in order as listed below
        # ac:  8 bit
        # xr:  8 bit
        # yr:  8 bit
        # sr:  8 bit
        # sp:  8 bit (set to 255 below)
        self.registers[4] = 255
