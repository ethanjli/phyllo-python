"""Ray32sub8 CRC calculation.

Ray32sub8, described in https://users.ece.cmu.edu/~koopman/pubs/ray06_crcalgorithms.pdf
and https://users.ece.cmu.edu/~koopman/crc/crc32.html, has HD=6 on data < 343 byte
s (which is beyond max packet length) and is optimized for embedded systems.
"""

# Builtins

# Packages


def reflect(data, num_bits):
    """Reflect a number by bit positions."""
    reflection = 0x0
    for bit in range(num_bits):
        if data & 0x1:
            reflection = reflection | (1 << (num_bits - 1 - bit))
        data = data >> 1
    return reflection


def generate_reflected_table(polynomial, num_bits=32):
    """Generate CRC byte lookup table for a given polynomial."""
    table = [0 for i in range(256)]
    reflected_polynomial = reflect(polynomial, num_bits)

    for dividend in range(256):
        byte = dividend
        for bit in range(8):
            if byte & 0x1:
                byte = byte >> 1
                byte = byte ^ reflected_polynomial
            else:
                byte = byte >> 1
        table[dividend] = byte

    return table


CRC32SUB8_POLYNOMIAL = 0x01ED
CRC32SUB8_REFLECTED_TABLE = generate_reflected_table(CRC32SUB8_POLYNOMIAL, 32)


def compute_reflected_crc(
        buffer, table=CRC32SUB8_REFLECTED_TABLE,
        initial_remainder=0xFFFFFFFF, final_xor=0xFFFFFFFF
):
    """Compute 32-bit reflected crc using a lookup table."""
    remainder = initial_remainder
    for byte in buffer:
        data = byte ^ (remainder & 0xFF)
        remainder = table[data] ^ (remainder >> 8)

    return remainder ^ final_xor


if __name__ == '__main__':
    assert compute_reflected_crc(b'123456789') == 0xB303B455
