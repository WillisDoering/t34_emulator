import memory as mem
import operations as op

opc_table = {
    10: op.asl_a,   # 0A
    72: op.pha,     # 48
    152: op.tya,    # 98
    200: op.iny,    # C8
    234: op.nop,    # EA
}



def prog_run(e_mem, user_in):
    # Setup program execution
    pc = int(user_in[0:-1], 16)
    e_mem.pc = pc
# Spacer  |123456789|123456789|123456789|123456789|123456789|
    print("PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")

    # TODO: Add variables for all values in all fields printed

    # Run program until break
    while e_mem.memory[e_mem.pc] != 0:
        opc = e_mem.memory[e_mem.pc]

        func = opc_table.get(opc)
        func(e_mem)

        # TODO: run opcode and update pc