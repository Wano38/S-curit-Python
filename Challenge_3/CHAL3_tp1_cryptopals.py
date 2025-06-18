# Chaîne hexadécimale chiffrée par XOR avec un seul caractère
hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

# Conversion en bytes
cipher_bytes = bytes.fromhex(hex_string)


letter_freq = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
    'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
    'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
    'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
    'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
    'y': 0.01974, 'z': 0.00074, ' ': 0.13
}

def score_text(text):
    """Attribue un score au texte selon la fréquence des caractères anglais"""
    return sum(letter_freq.get(c.lower(), 0) for c in text)

def xor_with_key(data, key):
    """XOR entre les bytes et une seule clé (int)"""
    return bytes([b ^ key for b in data])

def find_best_key(cipher_bytes):
    best_score = 0
    best_key = None
    best_message = ""

    for key in range(256):
        xored = xor_with_key(cipher_bytes, key)
        try:
            decoded = xored.decode("ascii")
        except UnicodeDecodeError:
            continue

        score = score_text(decoded)
        if score > best_score:
            best_score = score
            best_key = key
            best_message = decoded

    return best_key, chr(best_key), best_message

def main():
    key_val, key_char, message = find_best_key(cipher_bytes)
    print(f"Clé trouvée : {key_val} (char: '{key_char}')")
    print(f"Message : {message}")

if __name__ == "__main__":
    main()
