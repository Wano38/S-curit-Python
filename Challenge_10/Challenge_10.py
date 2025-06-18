from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

BLOCK_SIZE = 16
KEY = b"YELLOW SUBMARINE"
IV = b"\x00" * BLOCK_SIZE

# XOR entre deux blocs de même taille
def xor_bytes(block1, block2):
    return bytes(a ^ b for a, b in zip(block1, block2))

# Chiffrement ECB d'un bloc
def ecb_encrypt(block, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)

# Déchiffrement ECB d'un bloc
def ecb_decrypt(block, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)

# Chiffrement CBC manuel
def cbc_encrypt(plaintext, key, iv):
    plaintext = pad(plaintext, BLOCK_SIZE)
    blocks = [plaintext[i:i + BLOCK_SIZE] for i in range(0, len(plaintext), BLOCK_SIZE)]

    ciphertext = b""
    previous = iv

    for block in blocks:
        xored = xor_bytes(block, previous)
        encrypted = ecb_encrypt(xored, key)
        ciphertext += encrypted
        previous = encrypted

    return ciphertext

# Déchiffrement CBC manuel
def cbc_decrypt(ciphertext, key, iv):
    if len(ciphertext) == 0:
        raise ValueError("Le texte chiffré est vide.")

    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Le texte chiffré n'est pas un multiple de 16 octets.")

    blocks = [ciphertext[i:i + BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]

    plaintext = b""
    previous = iv

    for block in blocks:
        decrypted = ecb_decrypt(block, key)
        xored = xor_bytes(decrypted, previous)
        plaintext += xored
        previous = block

    return unpad(plaintext, BLOCK_SIZE)

# ======== Traitement du fichier test.txt =========

file_path = "test.txt"

if not os.path.exists(file_path):
    print("Erreur : Le fichier test.txt est introuvable.")
    exit()

with open(file_path, "rb") as f:
    raw_data = f.read()

# Tentative de décodage base64
try:
    ciphertext = base64.b64decode(raw_data)
    print("[Info] Données décodées comme base64.")
except Exception:
    ciphertext = raw_data
    print("[Info] Données utilisées telles quelles (pas base64).")

print(f"[Info] Longueur du ciphertext : {len(ciphertext)} octets")

# Déchiffrement CBC
try:
    decrypted = cbc_decrypt(ciphertext, KEY, IV)
    print("\n--- Texte déchiffré ---")
    print(decrypted.decode(errors="replace"))
except Exception as e:
    print(f"Erreur lors du déchiffrement : {e}")
