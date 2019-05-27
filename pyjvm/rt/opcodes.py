class PyOpCode(object):
    def __init__(self, name, opcode, params=0):
        self.name = name
        self.opcode = opcode
        self.params = params

    def __str__(self):
        return "PyOpCode(name={}, opcode={}, params={})".format(self.name, self.opcode, self.params)


OPCODES = {
    0x01    :   PyOpCode("ACONST_NULL", 0x01),
    0x19    :   PyOpCode("ALOAD",       0x19, 1),
    0x2a    :   PyOpCode("ALOAD_0",     0x2a, 1),
    0x2b    :   PyOpCode("ALOAD_1",     0x02b, 1),
    0xb0    :   PyOpCode("ARETURN",     0xb0),
    0x53    :   PyOpCode("ASTORE",      0x53),
    0x4b    :   PyOpCode("ASTORE_0",    0x4b),
    0x4c    :   PyOpCode("ASTORE_1",    0x4c),
    0x10    :   PyOpCode("BIPUSH",      0x10, 1),
    0xca    :   PyOpCode("BREAKPOINT",  0xca),
    0x63    :   PyOpCode("DADD",        0x63),
    0x67    :   PyOpCode("DSUB",        0x67),
    0x6b    :   PyOpCode("DMUL",        0x6b),
    0x6f    :   PyOpCode("DDIV",        0x6f),
    0x77    :   PyOpCode("DNEG",        0x77),
    0x73    :   PyOpCode("DREM",        0x73),
    0x0e    :   PyOpCode("DCONST_0",    0x0e), #?
    0x0f    :   PyOpCode("DCONST_1",    0x0f), #?
    0x18    :   PyOpCode("DLOAD",       0x18, 1),
    0x26    :   PyOpCode("DLOAD_0",     0x26),
    0x27    :   PyOpCode("DLOAD_1",     0x27),
    0x28    :   PyOpCode("DLOAD_2",     0x28),
    0x23    :   PyOpCode("DLOAD_3",     0x29),
    0xaf    :   PyOpCode("DRETURN",     0xaf), #?
    0x39    :   PyOpCode("DSTORE",      0x39, 1),
    0x47    :   PyOpCode("DSTORE_0",    0x47),
    0x48    :   PyOpCode("DSTORE_1",    0x48),
    0x49    :   PyOpCode("DSTORE_2",    0x49),
    0x4a    :   PyOpCode("DSTORE_3",    0x4a),
    0x59    :   PyOpCode("DUP",         0x59),
    0x5a    :   PyOpCode("DUP_X1",      0x5a),
    0x5b    :   PyOpCode("DUP_X2",      0x5b),
    0x5c    :   PyOpCode("DUP2",        0x5c),
    0x5d    :   PyOpCode("DUP2_X1",     0x5d),
    0x5e    :   PyOpCode("DUP2_X2",     0x5e),
    0xb4    :   PyOpCode("GETFIELD",    0xb4, 2),
    0xb2    :   PyOpCode("GETSTATIC",   0xb2, 2),
    0xa7    :   PyOpCode("GOTO",        0xa7, 2),
    0x87    :   PyOpCode("I2D",         0x87),
    0x60    :   PyOpCode("IADD",        0x60),
    0x7e    :   PyOpCode("IAND",        0x7e),
    0x02    :   PyOpCode("ICONST_M1",   0x02),
    0x03    :   PyOpCode("ICONST_0",    0x03),
    0x04    :   PyOpCode("ICONST_1",    0x04),
    0x05    :   PyOpCode("ICONST_2",    0x05),
    0x06    :   PyOpCode("ICONST_3",    0x06),
    0x07    :   PyOpCode("ICONST_4",    0x07),
    0x08    :   PyOpCode("ICONST_5",    0x08),
    0x6c    :   PyOpCode("IDIV",        0x6c),
    0x9f    :   PyOpCode("IF_ICMPEQ",   0x9f, 2),
    0xa0    :   PyOpCode("IF_ICMPNE",   0xa0, 2),
    0xa1    :   PyOpCode("IF_ICMPLT",   0xa1, 2),
    0xa2    :   PyOpCode("IF_ICMPGE",   0xa2, 2),
    0xa3    :   PyOpCode("IF_ICMPGT",   0xa3, 2),
    0xa4    :   PyOpCode("IF_ICMPLE",   0xa4, 2),
    0x99    :   PyOpCode("IFEQ",        0x99, 2),
    0x9c    :   PyOpCode("IFGE",        0x9c, 2),
    0x9d    :   PyOpCode("IFGT",        0x9d, 2),
    0x9e    :   PyOpCode("IFLE",        0x9d, 2),
    0x9b    :   PyOpCode("IFLT",        0x9b, 2),
    0x9a    :   PyOpCode("IFNE",        0x9a, 2),
    0xc7    :   PyOpCode("IFNONNULL",   0xc7, 2),
    0xc6    :   PyOpCode("IFNULL",      0xc6, 2),
    0x84    :   PyOpCode("IINC",        0x84, 2),
    0x15    :   PyOpCode("ILOAD",       0x15, 1),
    0x1a    :   PyOpCode("ILOAD_0",     0x1a),
    0x1b    :   PyOpCode("ILOAD_1",     0x1b),
    0x1c    :   PyOpCode("ILOAD_2",     0x1c),
    0x1d    :   PyOpCode("ILOAD_3",     0x1d),
    0xfe    :   PyOpCode("IMPDEP1",     0xfe), #?
    0xff    :   PyOpCode("IMPDEP2",     0xff), #?
    0x68    :   PyOpCode("IMUL",        0x68),
    0x74    :   PyOpCode("INEG",        0x74),
    0xb7    :   PyOpCode("INVOKESPECIAL",   0xb7),
    0xb8    :   PyOpCode("INVOKESTATIC",    0xb8),
    0xb6    :   PyOpCode("INVOKEVIRTUAL",   0xb6),
    0x80    :   PyOpCode("IOR",         0x80), #?
    0x70    :   PyOpCode("IREM",        0x70), #?
    0xac    :   PyOpCode("IRETURN",     0xac),
    0x36    :   PyOpCode("ISTORE",      0x36, 1),
    0x3b    :   PyOpCode("ISTORE_0",    0x3b),
    0x3c    :   PyOpCode("ISTORE_1",    0x3c),
    0x3d    :   PyOpCode("ISTORE_2",    0x3d),
    0x3e    :   PyOpCode("ISTORE_3",    0x3e),
    0x64    :   PyOpCode("ISUB",        0x64),
    0xc2    :   PyOpCode("MONITORENTER",0xc2),
    0xc3    :   PyOpCode("MONITOREXIT", 0xc3),
    0xbb    :   PyOpCode("NEW",         0xbb, 2),
    0xa8    :   PyOpCode("JSR",         0xa8, 2), #?
    0xc9    :   PyOpCode("JSR_W",       0xc9, 2), #?
    0x12    :   PyOpCode("LDC",         0x12, 1), #?
    0x00    :   PyOpCode("NOP",         0x00),    #?
    0x57    :   PyOpCode("POP",         0x57),    #?
    0x58    :   PyOpCode("POP2",        0x58),    #?
    0xb5    :   PyOpCode("PUTFIELD",    0xb5, 2),
    0xb3    :   PyOpCode("PUTSTATIC",   0xb3, 2),
    0xa9    :   PyOpCode("RET",         0xa9, 1),
    0xb1    :   PyOpCode("RETURN",      0xb1),
    0x11    :   PyOpCode("SIPUSH",      0x11, 2),
    0x5f    :   PyOpCode("SWAP",        0x5f),
}