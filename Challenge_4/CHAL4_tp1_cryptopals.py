def get_char_priority_score(text):
    etaoin_order = "etaoinshrdlu"
    score = 0
    for c in text.lower():
        if c in etaoin_order:
            score += 12 - etaoin_order.index(c)  # e = 12 pts, u = 1 pt
        elif c == ' ':
            score += 2  # on valorise aussi un peu l'espace
    return score

def xor_with_key(data_bytes, key):
    return bytes([b ^ key for b in data_bytes])

def find_best_key_for_line(hex_line):
    try:
        cipher_bytes = bytes.fromhex(hex_line.strip())
    except ValueError:
        return 0, None, ""

    best_score = 0
    best_key = None
    best_message = ""

    for key in range(256):
        xored = xor_with_key(cipher_bytes, key)
        try:
            decoded = xored.decode("ascii")
        except UnicodeDecodeError:
            continue

        score = get_char_priority_score(decoded)
        if score > best_score:
            best_score = score
            best_key = key
            best_message = decoded

    return best_score, best_key, best_message

def find_best_line_from_file(filepath):

    best_overall = (0, None, "", 0)

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            score, key, message = find_best_key_for_line(line)
            if score > best_overall[0]:
                best_overall = (score, key, message, line_num)

    return best_overall

def print_decryption_result(score, key, message, line_num):
    """Affiche les résultats du décryptage"""
    if key is not None:
        print(f"[Ligne {line_num}] Clé trouvée : {key} (char: '{chr(key)}')")
        print(f"Message : {message}")
    else:
        print("Aucun message valide trouvé.")

def main():
    filepath = "chal4.txt"
    score, key, message, line_num = find_best_line_from_file(filepath)
    print_decryption_result(score, key, message, line_num)

if __name__ == "__main__":
    main()
