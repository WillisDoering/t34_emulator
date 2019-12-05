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


# Returns result and flags for addition
def sign_add(op1, op2):
    flags = 32
    if op1 & 128:
        op1 = op1 & 127
        op1 -= 128

    if op2 & 128:
        op2 = op2 & 127
        op2 -= 128

    result = op1 + op2

    if result == 0:
        flags = flags | 2
    elif result > 127:
        result -= 128
        flags = flags | 65
    elif result < 0:
        result += 128
        flags = flags | 128
        if result < 0:
            result += 128
            flags = flags | 64

    return result, flags


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


# 08: Push Processor Status on Stack
def php(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.memory[e_mem.registers[4] + 256] = e_mem.registers[3]
    e_mem.registers[4] -= 1
    op_print(pc, "08", "PHP", "impl", "-- --", e_mem)


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


# 28: Pull Processor Status from Stack
def plp(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[4] += 1
    e_mem.registers[3] = e_mem.memory[e_mem.registers[4] + 256]
    op_print(pc, "28", "PLP", "impl", "-- --", e_mem)


# 2A: Rotate One Bit Left (Accumulator)
def rol_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    if e_mem.registers[3] & 1:
        carry_in = True
    else:
        carry_in = False
    e_mem.registers[3] = e_mem.registers[3] & 124

    if e_mem.registers[0] & 128:
        carry_out = True
    else:
        carry_out = False
    e_mem.registers[0] = (e_mem.registers[0] & 127) << 1
    if carry_in:
        e_mem.registers[0] = e_mem.registers[0] | 1
    if carry_out:
        e_mem.registers[3] = e_mem.registers[3] | 1
    if e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
    elif e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "2A", "ROL", "   A", "-- --", e_mem)


# 38: Set Carry Flag
def sec(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] | 1
    op_print(pc, "38", "SEC", "impl", "-- --", e_mem)


# 48: Push Accumulator on Stack
def pha(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    stack = 256 + e_mem.registers[4]
    e_mem.memory[stack] = e_mem.registers[0]
    e_mem.registers[4] -= 1
    op_print(pc, "48", "PHA", "impl", "-- --", e_mem)


# 4A: Shift One Bit Right (Accumulator)
def lsr_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 252
    if e_mem.registers[0] & 1:
        e_mem.registers[3] = e_mem.registers[3] | 1
        e_mem.registers[0] = e_mem.registers[0] & 254
    e_mem.registers[0] = e_mem.registers[0] >> 1
    if e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "4A", "LSR", "   A", "-- --", e_mem)


# 58: Clear Interrupt Disable Bit
def cli(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 251
    op_print(pc, "58", "CLI", "impl", "-- --", e_mem)


# 65: Add Memory to Accumulator with Carry (zeropage)
def adc_zpg(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[e_mem.pc + 1]
    e_mem.pc += 2
    e_mem.registers[3] = e_mem.registers[3] & 60

    e_mem.registers[0], flags = sign_add(e_mem.memory(op1), e_mem.registers[0])
    e_mem.registers[3] = e_mem.registers[3] | flags

    oprnd = ('{:02X}'.format(op1) + " --")
    op_print(pc, "65", "ADC", " zpg", oprnd, e_mem)


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


# 69: Add Memory to Accumulator with Carry (immediate)
def adc_imme(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[e_mem.pc + 1]
    e_mem.pc += 2
    e_mem.registers[3] = e_mem.registers[3] & 60

    e_mem.registers[0], flags = sign_add(op1, e_mem.registers[0])
    e_mem.registers[3] = e_mem.registers[3] | flags

    oprnd = ('{:02X}'.format(op1) + " --")
    op_print(pc, "69", "ADC", "   #", oprnd, e_mem)


# 6A: Rotate One Bit Right (Accumulator)
def ror_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    if e_mem.registers[3] & 1:
        carry_in = True
    else:
        carry_in = False
    e_mem.registers[3] = e_mem.registers[3] & 124

    if e_mem.registers[0] & 1:
        carry_out = True
    else:
        carry_out = False
    e_mem.registers[0] = (e_mem.registers[0] & 255) >> 1
    if carry_in:
        e_mem.registers[0] = e_mem.registers[0] | 128
    if carry_out:
        e_mem.registers[3] = e_mem.registers[3] | 1
    if e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128
    elif e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    op_print(pc, "6A", "ROR", "   A", "-- --", e_mem)


# 6C: Jump to New Location (indirect)
def jmp_ind(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[pc + 1]
    op2 = e_mem.memory[pc + 2]

    addr_loc = (op2 * 256) + op1
    e_mem.pc = (e_mem.memory[addr_loc + 1] * 256) + e_mem.memory[addr_loc]

    oprnd = ('{:02X}'.format(op1) + ' ' + '{:02X}'.format(op2))
    op_print(pc, "6C", "JMP", " ind", oprnd, e_mem)


# 6D: Add Memory to Accumulator with Carry (absolute)
def adc_abs(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[e_mem.pc + 1]
    op2 = e_mem.memory[e_mem.pc + 2]
    e_mem.pc += 3
    e_mem.registers[3] = e_mem.registers[3] & 60

    e_mem.registers[0], flags = sign_add(e_mem.memory[(op2 * 256) + op1], e_mem.registers[0])
    e_mem.registers[3] = e_mem.registers[3] | flags

    oprnd = ('{:02X}'.format(op1) + ' ' + '{:02X}'.format(op2))
    op_print(pc, "6D", "ADC", " abs", oprnd, e_mem)


# 78: Set Interrupt Disable Status
def sei(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] | 4
    op_print(pc, "78", "SEI", "impl", "-- --", e_mem)


# 85: Store Accumulator in Memory (zeropage)
def sta_zpg(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[e_mem.pc + 1]
    e_mem.pc += 2

    e_mem.memory[op1] = e_mem.registers[0]

    oprnd = ('{:02X}'.format(op1) + " --")
    op_print(pc, "85", "STA", " zpg", oprnd, e_mem)


# 88: Decrement Index Y by One
def dey(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    if e_mem.registers[2] & 128:
        e_mem.registers[2] -= 1
        if e_mem.registers[2] < 128:
            e_mem.registers[2] = 0
        else:
            e_mem.registers[3] = e_mem.registers[3] | 128
    else:
        if e_mem.registers[2] == 0:
            e_mem.registers[2] = 255
            e_mem.registers[3] = e_mem.registers[3] | 128
        else:
            e_mem.registers[2] -= 1
    if e_mem.registers[2] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2

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


# 9A: Transfer Index X to Stack Register
def txs(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[4] = e_mem.registers[1]
    op_print(pc, "9A", "TXS", "impl", "-- --", e_mem)


# A2: Load Index X with Memory (immediate)
def ldx_imme(e_mem):
    pc = e_mem.pc
    flag_set = 0
    op1 = e_mem.memory[e_mem.pc + 1]
    e_mem.pc += 2
    e_mem.registers[3] = e_mem.registers[3] & 125

    e_mem.registers[1] = op1
    if e_mem.registers[1] & 128:
        flag_set += 128
    if e_mem.registers[1] == 0:
        flag_set += 0
    e_mem.registers[3] = e_mem.registers[3] | flag_set

    oprnd = ('{:02X}'.format(op1) + " --")
    op_print(pc, "A2", "LDX", "   #", oprnd, e_mem)


# A5: Load Accumulator with memory (zeropage)
def lda_zpg(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[e_mem.pc + 1]
    e_mem.pc += 2
    e_mem.registers[3] = e_mem.registers[3] & 125

    e_mem.registers[0] = e_mem.memory[op1]
    if e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    elif e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128

    oprnd = ('{:02X}'.format(op1) + " --")
    op_print(pc, "A5", "LDA", " zpg", oprnd, e_mem)


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
    op_print(pc, "AA", "TAX", "impl", "-- --", e_mem)


# AD: Load Accumulator with Memory (absolute)
def lda_abs(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[e_mem.pc + 1]
    op2 = e_mem.memory[e_mem.pc + 2]
    e_mem.pc += 3
    e_mem.registers[3] = e_mem.registers[3] & 125

    e_mem.registers[0] = e_mem.memory[(op2 * 256) + op1]
    if e_mem.registers[0] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2
    elif e_mem.registers[0] & 128:
        e_mem.registers[3] = e_mem.registers[3] | 128

    oprnd = ('{:02X}'.format(op1) + ' ' + '{:02X}'.format(op2))
    op_print(pc, "AD", "LDA", " abs", oprnd, e_mem)


# B8: Clear Overflow Flag
def clv(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 191
    op_print(pc, "B8", "CLV", "impl", "-- --", e_mem)


# BA: Transfer Stack Pointer to Index X
def tsx(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[1] = e_mem.registers[4]
    op_print(pc, "BA", "TSX", "impl", "-- --", e_mem)


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


# CA: Decrement Index X by One
def dex(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
    if e_mem.registers[1] & 128:
        e_mem.registers[1] -= 1
        if e_mem.registers[1] < 128:
            e_mem.registers[1] = 0
        else:
            e_mem.registers[3] = e_mem.registers[3] | 128
    else:
        if e_mem.registers[1] == 0:
            e_mem.registers[1] = 255
            e_mem.registers[3] = e_mem.registers[3] | 128
        else:
            e_mem.registers[1] -= 1
    if e_mem.registers[1] == 0:
        e_mem.registers[3] = e_mem.registers[3] | 2

    op_print(pc, "CA", "DEX", "impl", "-- --", e_mem)


# D0: Branch on Result not Zero
def bne(e_mem):
    pc = e_mem.pc
    op1 = e_mem.memory[e_mem.pc + 1]
    e_mem.pc += 2
    if e_mem.registers[3] & 64:
        if e_mem.pc < 128:
            e_mem.pc += op1
        else:
            op1 = op1 & 127
            op1 -= 128
            e_mem.pc += op1
    else:
        e_mem.pc += 2

    oprnd = ('{:02X}'.format(op1) + " --")
    op_print(pc, "D0", "BNE", " rel", oprnd, e_mem)


# D8: Clear Decimal Mode
def cld(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 247
    op_print(pc, "D8", "CLD", "impl", "-- --", e_mem)


# E6: Increment Memory by One (zeropage)
def inc_zpg(e_mem):
    pc = e_mem.pc
    flags = 0
    op1 = e_mem.memory[e_mem.pc + 1]
    e_mem.pc += 2
    e_mem.registers[3] = e_mem.registers[3] & 125

    e_mem.memory[op1] += 1
    if e_mem.memory[op1] == 0:
        flags += 2
    elif e_mem.memory[op1] > 127:
        e_mem.memory[op1] = 0
        flags += 128

    e_mem.registers[3] = e_mem.registers[3] | flags

    oprnd = ('{:02X}'.format(op1) + " --")
    op_print(pc, "E6", "INC", " zpg", oprnd, e_mem)


# E8: Increment Index X by One
def inx(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] & 125
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


# F8: Set Decimal Flag
def sed(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1
    e_mem.registers[3] = e_mem.registers[3] | 8
    op_print(pc, "F8", "SED", "impl", "-- --", e_mem)