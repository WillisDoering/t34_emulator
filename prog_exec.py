import memory as mem
import operations as op

opc_table = {
    0:   op.brk,        # 00
    8:   op.php,        # 08
    10:  op.asl_a,      # 0A
    24:  op.clc,        # 18
    40:  op.plp,        # 28
    42:  op.rol_a,      # 2A
    56:  op.sec,        # 38
    72:  op.pha,        # 48
    74:  op.lsr_a,      # 4A
    58:  op.cli,        # 58
    104: op.pla,        # 68
    105: op.adc_imme,   # 69
    106: op.ror_a,      # 6A
    120: op.sei,        # 78
    136: op.dey,        # 88
    138: op.txa,        # 8A
    152: op.tya,        # 98
    154: op.txs,        # 9A
    162: op.ldx_imme,   # A2
    168: op.tay,        # A8
    170: op.tax,        # AA
    184: op.clv,        # B8
    186: op.tsx,        # BA
    200: op.iny,        # C8
    202: op.dex,        # CA
    216: op.cld,        # D8
    232: op.inx,        # E8
    234: op.nop,        # EA
    248: op.sed,        # F8
}


def prog_run(e_mem, user_in):
    # Setup program execution
    pc = int(user_in[0:-1], 16)
    e_mem.pc = pc
    e_mem.registers[3] = e_mem.registers[3] & 32

# Spacer  |123456789|123456789|123456789|123456789|123456789|
    print("PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")

    # Run program until break
    while not (e_mem.registers[3] & 4):
        opc = e_mem.memory[e_mem.pc]

        func = opc_table.get(opc, op.inv_error)
        func(e_mem)