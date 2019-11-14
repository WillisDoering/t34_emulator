def op_print(pc, op, ins, amod, oprnd, e_mem):
    print('{:03X}'.format(pc), '', op, '', ins, ' ', amod, oprnd, '',
          '{:02X}'.format(e_mem.registers[0]),
          '{:02X}'.format(e_mem.registers[1]),
          '{:02X}'.format(e_mem.registers[2]),
          '{:02X}'.format(e_mem.registers[4]),
          '{:08b}'.format(e_mem.registers[3]))


def asl_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1

    op_print(pc, "0A", "ASL", "   A", "-- --", e_mem)


def nop(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1

    op_print(pc, "EA", "NOP", "impl", "-- --", e_mem)
