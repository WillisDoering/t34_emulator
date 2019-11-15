def op_print(pc, op, ins, amod, oprnd, e_mem):
    print('{:03X}'.format(pc), '', op, '', ins, ' ', amod, oprnd, '',
          '{:02X}'.format(e_mem.registers[0]),
          '{:02X}'.format(e_mem.registers[1]),
          '{:02X}'.format(e_mem.registers[2]),
          '{:02X}'.format(e_mem.registers[4]),
          '{:08b}'.format(e_mem.registers[3]))


def inv_error(e_mem):
    print("Invalid Operation", e_mem.memory[e_mem.pc])
    e_mem.pc += 1


def asl_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    op_print(pc, "0A", "ASL", "   A", "-- --", e_mem)


# 48: Push Accumulator on Stack
def pha(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    stack = 256 + e_mem.registers[4]
    e_mem.memory[stack] = e_mem.registers[0]
    e_mem.registers[4] -= 1
    op_print(pc, "48", "PHA", "impl", "-- --", e_mem)


# 98: Transfer Index Y to Accumulator
def tya(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[0] = e_mem.registers[2]
    op_print(pc, "EA", "NOP", "impl", "-- --", e_mem)


# C8: Increment Index Y by One
def iny(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[2] += 1
    op_print(pc, "C8", "INY", "impl", "-- --", e_mem)


# EA: No Operation
def nop(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    op_print(pc, "EA", "NOP", "impl", "-- --", e_mem)
