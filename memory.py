# The class below holds the memory and registers for the emulator


# Status register (sr) is formatted with NV-BDIZC
class Memory:
    def __init__(self, mem_size, pc, ac, x, y, sr, sp):
        self.memory = bytearray(mem_size)
        self.pc = bytes(2)    # 16 bit
        self.ac = bytes(1)    # 8 bit
        self.x = bytes(1)     # 8 bit
        self.y = bytes(1)     # 8 bit
        self.sr = bytes(1)    # 8 bit, Format: NV-BDIZC
        self.sp = bytes(1)    # 8 bit
