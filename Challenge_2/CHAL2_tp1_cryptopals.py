Data = "1c0111001f010100061a024b53535009181c"
Data2 = "686974207468652062756c6c277320657965"

def xor_hex_strings(hex1, hex2):
    bytes1 = bytes.fromhex(hex1)
    bytes2 = bytes.fromhex(hex2)

    if len(bytes1) != len(bytes2):
        raise ValueError("Les deux chaînes hex doivent être de même longueur")

    xor_result = bytes(a ^ b for a, b in zip(bytes1, bytes2))

    return xor_result.hex()

def main():
    result = xor_hex_strings(Data, Data2)
    print("Résultat du XOR (hex) :", result)

if __name__ == "__main__":
    main()