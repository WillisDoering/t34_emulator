import memory as mem


def prog_run(e_mem, user_in):
    # Setup program execution
    pc = user_in[0:-1]
    e_mem.pc = int(pc, 16)
# Spacer  |123456789|123456789|123456789|123456789|123456789|
    print("PC  OPC  INS   AMOD OPRND  AC  XR YR SP NV-BDIZC")

    # Run program until break
    while e_mem.pc != 0:
        # run opcode and update pc
        e_mem.pc = 0    # remove when functional
