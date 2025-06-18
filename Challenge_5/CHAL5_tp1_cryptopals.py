def repeating_key_xor(plaintext: str, key: str) -> str:
    ciphertext = []
    key_bytes = key.encode()
    key_len = len(key_bytes)

    # ciphertext = bytes(b ^ key_bytes[i % key_len] for i, b in enumerate(plaintext.encode()))
    for i, char in enumerate(plaintext.encode()):
        xor_byte = char ^ key_bytes[i % key_len]
        ciphertext.append(f"{xor_byte:02x}")

    return ''.join(ciphertext)


# Test input
plaintext = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

key = "ICE"
cipher_hex = repeating_key_xor(plaintext, key)
print(cipher_hex)