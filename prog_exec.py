import memory as mem
import operations as op

opc_table = {
    0x00: op.brk,
    0x06: op.asl_zpg,
    0x08: op.php,
    0x09: op.ora_imme,
    0x0A: op.asl_a,
    0x18: op.clc,
    0x20: op.jsr,
    0x25: op.and_zpg,
    0x28: op.plp,
    0x29: op.and_imme,
    0x2A: op.rol_a,
    0x38: op.sec,
    0x46: op.lsr_zpg,
    0x48: op.pha,
    0x49: op.eor_imme,
    0x4A: op.lsr_a,
    0x4C: op.jmp_abs,
    0x58: op.cli,
    0x60: op.rts,
    0x65: op.adc_zpg,
    0x68: op.pla,
    0x69: op.adc_imme,
    0x6A: op.ror_a,
    0x6C: op.jmp_ind,
    0x6D: op.adc_abs,
    0x78: op.sei,
    0x84: op.sty_zpg,
    0x85: op.sta_zpg,
    0x86: op.stx_zpg,
    0x88: op.dey,
    0x8A: op.txa,
    0x8D: op.sta_abs,
    0x90: op.bcc,
    0x98: op.tya,
    0x9A: op.txs,
    0xA0: op.ldy_imme,
    0xA2: op.ldx_imme,
    0xA5: op.lda_zpg,
    0xA6: op.ldx_zpg,
    0xA8: op.tay,
    0xA9: op.lda_imme,
    0xAA: op.tax,
    0xAD: op.lda_abs,
    0xB8: op.clv,
    0xBA: op.tsx,
    0xC6: op.dec_zpg,
    0xC8: op.iny,
    0xC9: op.cmp_imme,
    0xCA: op.dex,
    0xD0: op.bne,
    0xD8: op.cld,
    0xE6: op.inc_zpg,
    0xE9: op.sbc_imme,
    0xE8: op.inx,
    0xEA: op.nop,
    0xF8: op.sed,
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