# Implémentation du remplissage PKCS#7
TEXT = "SOUS-MARIN JAUNE"
BLOCK_SIZE = 20

def pkcs7_pad(text, block_size):
    data = text.encode('utf-8')
    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len]) * padding_len
    padded_data = data + padding
    print(padded_data)
    return padded_data

def main():
    pkcs7_pad(TEXT, BLOCK_SIZE)

if __name__ == "__main__":
    main()
