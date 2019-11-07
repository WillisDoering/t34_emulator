# The class below holds the memory and registers for the emulator


# Status register (sr) is formatted with NV-BDIZC
class Memory:
    def __init__(self, mem_size):
        self.memory = bytearray(mem_size)   # Memory
        self.registers = bytearray(7)       # All 6 registers in order as listed below
        # pc: 16 bit
        # ac:  8 bit
        # xr:  8 bit
        # yr:  8 bit
        # sr:  8 bit
        # sp:  8 bit (set to 255 below)
        self.registers[6] = 255
