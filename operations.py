def op_print(pc, op, ins, amod, oprnd, e_mem):
    print('{:03X}'.format(pc), '', op, '', ins, ' ', amod, oprnd, '',
          '{:02X}'.format(e_mem.registers[0]),
          '{:02X}'.format(e_mem.registers[1]),
          '{:02X}'.format(e_mem.registers[2]),
          '{:02X}'.format(e_mem.registers[4]),
          '{:08b}'.format(e_mem.registers[3]))


def inv_error(e_mem):
    print("Invalid Operation", '{:02X}'.format(e_mem.memory[e_mem.pc]))
    e_mem.registers[3] = e_mem.registers[3] | 4


# 00: Force Break
def brk(e_mem):
    pc = e_mem.pc
    e_mem.registers[3] = e_mem.registers[3] | 20
    pc_push = (e_mem.pc + 2) % 256
    e_mem.memory[e_mem.registers[4] + 256] = pc_push
    e_mem.registers[4] -= 1
    pc_push = int((e_mem.pc + 2) / 256)
    e_mem.memory[e_mem.registers[4] + 256] = pc_push
    e_mem.registers[4] -= 1
    e_mem.memory[e_mem.registers[4] + 256] = e_mem.registers[3]
    e_mem.registers[4] -= 1

    op_print(pc, "00", "BRK", "impl", "-- --", e_mem)


# 0A: Shift Left One Bit (Accumulator)
def asl_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 124
    if e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 1
        e_mem.registers[0] = e_mem.registers[0] & 127
    e_mem.registers[0] = e_mem.registers[0] << 1
    if e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
    if e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "0A", "ASL", "   A", "-- --", e_mem)


# 18: Clear Cary Flag
def clc(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 254
    op_print(pc, "18", "CLC", "impl", "-- --", e_mem)


# 2A: Rotate One Bit Left (Accumulator)
def rol_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 124
    roll_value = (e_mem.registers[0] & 128) >> 7
    e_mem.registers[0] = (e_mem.registers[0] & 127) << 1
    e_mem.registers[0] += roll_value
    if roll_value:
        e_mem.registers[3] = e_mem.registers[3] | 1
    if e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
    if e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "2A", "ROL", "   A", "-- --", e_mem)


# 48: Push Accumulator on Stack
def pha(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    stack = 256 + e_mem.registers[4]
    e_mem.memory[stack] = e_mem.registers[0]
    e_mem.registers[4] -= 1
    op_print(pc, "48", "PHA", "impl", "-- --", e_mem)


# 58: Clear Interrupt Disable Bit
def cli(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 251
    op_print(pc, "58", "CLI", "impl", "-- --", e_mem)


# 68: Pull Accumulator from Stack
def pla(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    e_mem.registers[4] += 1
    e_mem.registers[0] = e_mem.memory[e_mem.registers[4] + 256]
    if e_mem.registers[0] > 127:
        e_mem.registers[3] = e_mem.registers[3] | 128
    elif e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "68", "PLA", "impl", "-- --", e_mem)


# 6A: Rotate One Bit Right (Accumulator)
def ror_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 124
    roll_value = (e_mem.registers[0] & 1) << 7
    e_mem.registers[0] = (e_mem.registers[0] & 127) >> 1
    e_mem.registers[0] += roll_value
    if roll_value:
        e_mem.registers[3] = e_mem.registers[3] | 1
    if e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
    if e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "6A", "ROR", "   A", "-- --", e_mem)


# 88: Decrement Index Y by One
def dey(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    if e_mem.registers[2] & 128:
        e_mem.registers[2] -= 1
        if e_mem.registers[2] < 128:
            e_mem.registers[2] = 0
            e_mem.registers[3] = e_mem.registers[3] | 2
        else:
            e_mem.registers[3] = e_mem.registers[3] | 128
    else:
        if e_mem.registers[2] == 0:
            e_mem.registers[2] = 255
            e_mem.registers[3] = e_mem.registers[3] | 128
        else:
            e_mem.registers[2] -= 1

    op_print(pc, "88", "DEY", "impl", "-- --", e_mem)


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


# A8: Transfer Accumulator to Index Y
def tay(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    e_mem.registers[2] = e_mem.registers[0]
    if e_mem.registers[2] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
    if e_mem.registers[2] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "A8", "TAY", "impl", "-- --", e_mem)


# AA: Transfer Accumulator to Index X
def tax(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    e_mem.registers[1] = e_mem.registers[0]
    if e_mem.registers[1] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
    if e_mem.registers[1] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "A8", "TAY", "impl", "-- --", e_mem)


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


# D8: Clear Decimal Mode
def cld(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 247
    op_print(pc, "D8", "CLD", "impl", "-- --", e_mem)


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


# EA: No Operation
def nop(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    op_print(pc, "EA", "NOP", "impl", "-- --", e_mem)
