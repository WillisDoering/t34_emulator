# The class below holds the memory and registers for the emulator


# Status register (sr) is formatted with NV-BDIZC
class Memory:
    def __init__(self, memory, pc, ac, x, y, sr, sp):
        self.memory = memory
        self.pc = pc    # 16 bit
        self.ac = ac    # 8 bit
        self.x = x      # 8 bit
        self.y = y      # 8 bit
        self.sr = sr    # 8 bit, Format: NV-BDIZC
        self.sp = sp    # 8 bit
