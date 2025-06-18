import base64
from Crypto.Cipher import AES


def decrypt_aes_ecb_base64_from_file(filename, key):
    with open(filename, 'r') as f:
        base64_data = f.read().replace('\n', '')
    encrypted_data = base64.b64decode(base64_data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted_data)
    # Suppression du padding PKCS#7
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode('utf-8', errors='replace')


def main():
    key = b"YELLOW SUBMARINE"
    plaintext = decrypt_aes_ecb_base64_from_file("Chal7.txt", key)
    print(plaintext)


if __name__ == "__main__":
    main()
