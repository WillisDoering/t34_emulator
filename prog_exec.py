import memory as mem
import operations as op

opc_table = {
    0: op.brk,      # 00
    10: op.asl_a,   # 0A
    72: op.pha,     # 48
    104: op.pla,    # 68
    138: op.txa,    # 8A
    152: op.tya,    # 98
    200: op.iny,    # C8
    232: op.inx,    # E8
    234: op.nop,    # EA
}


def prog_run(e_mem, user_in):
    # Setup program execution
    pc = int(user_in[0:-1], 16)
    e_mem.pc = pc
    cont = True
# Spacer  |123456789|123456789|123456789|123456789|123456789|
    print("PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")

    # Run program until break
    while cont:
        opc = e_mem.memory[e_mem.pc]

        func = opc_table.get(opc, op.inv_error)
        cont = func(e_mem)

        # TODO: run opcode and update pc