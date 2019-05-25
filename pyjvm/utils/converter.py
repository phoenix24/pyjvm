def toint(byte):
    return int.from_bytes(
        byte,
        byteorder='little'
    )


def tostring(bytes):
    result = b''
    for x in bytes:
        result += x
    return str(result, 'utf-8')
