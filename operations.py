def op_print(pc, op, ins, amod, oprnd, e_mem):
    print('{:03X}'.format(pc), '', op, '', ins, ' ', amod, oprnd, '',
          '{:02X}'.format(e_mem.registers[0]),
          '{:02X}'.format(e_mem.registers[1]),
          '{:02X}'.format(e_mem.registers[2]),
          '{:02X}'.format(e_mem.registers[4]),
          '{:08b}'.format(e_mem.registers[3]))


def inv_error(e_mem):
    print("Invalid Operation", '{:02X}'.format(e_mem.memory[e_mem.pc]))
    return False


def asl_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    op_print(pc, "0A", "ASL", "   A", "-- --", e_mem)
    return True


# 48: Push Accumulator on Stack
def pha(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    stack = 256 + e_mem.registers[4]
    e_mem.memory[stack] = e_mem.registers[0]
    e_mem.registers[4] -= 1
    op_print(pc, "48", "PHA", "impl", "-- --", e_mem)
    return True


# 8A: Transfer Index X to Accumulator
def txa(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    e_mem.registers[0] = e_mem.registers[1]
    if e_mem.registers[0] > 127:
        e_mem.registers[3] = e_mem.registers[3] | 128
    elif e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "8A", "TXA", "impl", "-- --", e_mem)
    return True


# 98: Transfer Index Y to Accumulator
def tya(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    e_mem.registers[0] = e_mem.registers[2]
    if e_mem.registers[0] > 127:
        e_mem.registers[3] = e_mem.registers[3] | 128
    elif e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "98", "TYA", "impl", "-- --", e_mem)
    return True


# C8: Increment Index Y by One
def iny(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    if e_mem.registers[2] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
        e_mem.registers[2] += 1
        if e_mem.registers[2] == 0:
            e_mem.registers[3] = e_mem.registers[3] & 127
            e_mem.registers[3] = e_mem.registers[3] | 2
    else:
        e_mem.registers[2] += 1
        e_mem.registers[3] = e_mem.registers[3] & 127
        if e_mem.registers[2] > 127:
            e_mem.registers[2] = 0
            e_mem.registers[3] = e_mem.registers[3] | 2

    op_print(pc, "C8", "INY", "impl", "-- --", e_mem)
    return True


# E8: Increment Index X by One
def inx(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    if e_mem.registers[1] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
        e_mem.registers[1] += 1
        if e_mem.registers[1] == 0:
            e_mem.registers[3] = e_mem.registers[3] & 127
            e_mem.registers[3] = e_mem.registers[3] | 2
    else:
        e_mem.registers[1] += 1
        e_mem.registers[3] = e_mem.registers[3] & 127
        if e_mem.registers[1] > 127:
            e_mem.registers[1] = 0
            e_mem.registers[3] = e_mem.registers[3] | 2

    op_print(pc, "E8", "INX", "impl", "-- --", e_mem)
    return True


# EA: No Operation
def nop(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    op_print(pc, "EA", "NOP", "impl", "-- --", e_mem)
    return True
