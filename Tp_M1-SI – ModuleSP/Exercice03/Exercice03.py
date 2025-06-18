"""
Exercice 3 — Analyse des blocs chiffrés

1. Extraire les blocs de 16 octets de l’image chiffrée.
2. Compter combien de blocs sont identiques dans le fichier chiffré.
3. Afficher un histogramme de fréquence des blocs.

Questions :
• Quel mode présente le plus de répétitions ?
• Pourquoi ECB génère-t-il autant de blocs identiques ?
• En quoi cela compromet-il la confidentialité ?
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def encrypt_image_raw_bytes(image: Image.Image, key: bytes, mode: str):
    pixel_data = np.array(image)
    flat_bytes = pixel_data.tobytes()
    padded = pad(flat_bytes, AES.block_size)

    if mode == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
    elif mode == 'CBC':
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
    else:
        raise ValueError("Mode doit être 'ECB' ou 'CBC'")

    encrypted = cipher.encrypt(padded)
    return encrypted

def count_repeated_blocks(cipher_bytes: bytes, block_size=16):
    blocks = [cipher_bytes[i:i+block_size] for i in range(0, len(cipher_bytes), block_size)]
    block_counts = Counter(blocks)
    repeated_blocks = {b: c for b, c in block_counts.items() if c > 1}
    return block_counts, repeated_blocks

def plot_block_histogram(block_counts, mode):
    counts = list(block_counts.values())
    plt.figure(figsize=(8, 4))
    plt.hist(counts, bins=range(1, max(counts)+2), edgecolor='black', color='red')
    plt.title(f"Histogramme des fréquences de blocs ({mode})")
    plt.xlabel("Nombre d’occurrences d’un bloc")
    plt.ylabel("Nombre de blocs")
    plt.grid(True)
    plt.show()

def print_top_repeated_blocks(block_counts):
    print("\nTop 10 blocs les plus fréquents (hex) :")
    for block, count in block_counts.most_common(10):
        if count > 1:
            print(f"{block.hex()[:32]}... : {count} fois")

def afficher_reponses(mode, repeated_count):
    print(f"\n=== Analyse pour le mode {mode} ===")
    print(f"Blocs répétés : {len(repeated_count)}")
    print("• Quel mode présente le plus de répétitions ?")
    if mode == 'ECB':
        print("  → Le mode ECB montre beaucoup de répétitions.")
        print("• Pourquoi ECB génère-t-il autant de blocs identiques ?")
        print("  → Il chiffre chaque bloc indépendamment, donc des blocs identiques produisent un même résultat.")
        print("• En quoi cela compromet-il la confidentialité ?")
        print("  → Des motifs répétitifs dans l'image originale deviennent visibles dans l'image chiffrée.")
    else:
        print("  → CBC produit peu ou pas de blocs répétés.")
        print("• Grâce à l’IV et au chaînage, chaque bloc dépend du précédent.")
        print("• Cela renforce la confidentialité en supprimant les motifs visibles.")

def main():
    image_path = 'logo-linux.png'
    key = b'Sixteen byte key'
    img = Image.open(image_path).convert('RGB')

    for mode in ['ECB', 'CBC']:
        print(f"\n[*] Chiffrement de l'image en mode {mode}...")
        cipher_bytes = encrypt_image_raw_bytes(img, key, mode)

        print("[*] Extraction et comptage des blocs de 16 octets...")
        block_counts, repeated_blocks = count_repeated_blocks(cipher_bytes)

        total_blocks = len(cipher_bytes) // 16
        print(f"Nombre total de blocs : {total_blocks}")
        print(f"Nombre de blocs répétés : {len(repeated_blocks)}")

        plot_block_histogram(block_counts, mode)
        print_top_repeated_blocks(block_counts)
        afficher_reponses(mode, repeated_blocks)

if __name__ == "__main__":
    main()
