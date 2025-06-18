"""
Exercice 2 — Chiffrement CBC de la même image

1. Reprendre l’image utilisée dans l’exercice précédent.
2. Chiffrer cette image avec AES en mode CBC.
3. Utiliser un vecteur d’initialisation (IV) aléatoire de 16 octets.
4. Sauvegarder l’image chiffrée.
5. Comparer visuellement les deux images chiffrées (ECB vs CBC).

Questions :
• Que voyez-vous dans l’image chiffrée en CBC ?
• Pourquoi les motifs ont-ils disparu ?
• Quel est le rôle exact de l’IV dans ce mode ?
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def encrypt_pixels(image: Image.Image, key: bytes, mode: str):
    pixel_data = np.array(image)
    shape = pixel_data.shape
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
    encrypted = encrypted[:len(flat_bytes)]
    encrypted_pixels = np.frombuffer(encrypted, dtype=np.uint8).reshape(shape)
    return Image.fromarray(encrypted_pixels)

def display_comparison(original_img, ecb_img, cbc_img):
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.title("Image originale")
    plt.imshow(original_img)
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title("Chiffrement ECB")
    plt.imshow(ecb_img)
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("Chiffrement CBC")
    plt.imshow(cbc_img)
    plt.axis('off')

    plt.show()

def afficher_reponses():
    print("\n=== Réponses aux questions (CBC) ===")
    print("• Que voyez-vous dans l’image chiffrée en CBC ?")
    print("  → L’image semble complètement brouillée, sans motifs visibles.")
    print("• Pourquoi les motifs ont-ils disparu ?")
    print("  → Le mode CBC introduit de l'aléa entre les blocs, ce qui supprime les répétitions visibles.")
    print("• Quel est le rôle exact de l’IV dans ce mode ?")
    print("  → L’IV initialise le premier bloc de chiffrement, empêchant que deux messages identiques produisent le même résultat.")

def main():
    original_image_path = 'logo-linux.png'
    key = b'Sixteen byte key'

    print("[*] Chargement de l'image...")
    img = Image.open(original_image_path).convert('RGB')

    print("[*] Chiffrement ECB...")
    ecb_img = encrypt_pixels(img, key, 'ECB')

    print("[*] Chiffrement CBC avec IV aléatoire...")
    cbc_img = encrypt_pixels(img, key, 'CBC')

    print("[*] Affichage des images pour comparaison...")
    display_comparison(img, ecb_img, cbc_img)

    afficher_reponses()

if __name__ == "__main__":
    main()
