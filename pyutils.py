def toint(byte):
    return int.from_bytes(
        byte,
        byteorder='little'
    )
