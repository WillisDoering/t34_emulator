import memory as mem
import operations as op

opc_table = {
    0:   op.brk,        # 00
    10:  op.asl_a,      # 0A
    42:  op.rol_a,      # 2A
    72:  op.pha,        # 48
    104: op.pla,        # 68
    106: op.ror_a,      # 6A
    136: op.dey,        # 88
    138: op.txa,        # 8A
    152: op.tya,        # 98
    168: op.tay,        # A8
    200: op.iny,        # C8
    232: op.inx,        # E8
    234: op.nop,        # EA
}


def prog_run(e_mem, user_in):
    # Setup program execution
    pc = int(user_in[0:-1], 16)
    e_mem.pc = pc
    e_mem.registers[3] = e_mem.registers[3] & 251

# Spacer  |123456789|123456789|123456789|123456789|123456789|
    print("PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")

    # Run program until break
    while not (e_mem.registers[3] & 4):
        opc = e_mem.memory[e_mem.pc]

        func = opc_table.get(opc, op.inv_error)
        func(e_mem)