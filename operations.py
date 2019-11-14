def asl_a(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1

    print('{:03X}'.format(pc),
          " 0A  ASL      A -- -- ",
          '{:02X}'.format(e_mem.registers[0]),
          '{:02X}'.format(e_mem.registers[1]),
          '{:02X}'.format(e_mem.registers[2]),
          '{:02X}'.format(e_mem.registers[4]),
          '{:08b}'.format(e_mem.registers[3]))


def nop(e_mem):
    pc = e_mem.pc
    e_mem.pc += 1

    print('{:03X}'.format(pc),
          " 0A  NOP   impl -- -- ",
          '{:02X}'.format(e_mem.registers[0]),
          '{:02X}'.format(e_mem.registers[1]),
          '{:02X}'.format(e_mem.registers[2]),
          '{:02X}'.format(e_mem.registers[4]),
          '{:08b}'.format(e_mem.registers[3]))