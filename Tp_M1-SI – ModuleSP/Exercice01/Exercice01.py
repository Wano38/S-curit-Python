"""
1. Télécharger une image (par exemple Tux, un QR code ou un logo à motifs).
2. Convertir l’image en octets (bytes).
3. Chiffrer l’image avec AES en mode ECB avec une clé de 16 octets.
4. Sauvegarder l’image chiffrée.
5. Comparer visuellement l’image d’origine et l’image chiffrée.

Questions :
• Que remarquez-vous dans l’image chiffrée ?
• Pourquoi peut-on voir la forme d’origine ?
• Quelles données sont restées identifiables malgré le chiffrement ?
"""



from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def encrypt_pixels_ecb(image: Image.Image, key: bytes) -> Image.Image:
    # Convertir l'image en données RGB brutes
    pixel_data = np.array(image)
    shape = pixel_data.shape

    # Aplatir et transformer en bytes
    flat_bytes = pixel_data.tobytes()
    padded = pad(flat_bytes, AES.block_size)

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded)

    # Récupérer un tableau d'octets et le tronquer à la taille originale
    encrypted = encrypted[:len(flat_bytes)]
    encrypted_pixels = np.frombuffer(encrypted, dtype=np.uint8).reshape(shape)

    return Image.fromarray(encrypted_pixels)

def display_images(original_img, encrypted_img):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Image originale")
    plt.imshow(original_img)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title("Image chiffrée (ECB)")
    plt.imshow(encrypted_img)
    plt.axis('off')

    plt.show()

def afficher_reponses():
    print("\n=== Réponses aux questions ===")
    print("• Que remarquez-vous dans l’image chiffrée ?")
    print("  → Des motifs et formes de l’image d’origine sont encore visibles malgré le chiffrement.")
    print("• Pourquoi peut-on voir la forme d’origine ?")
    print("  → Le mode ECB chiffre chaque bloc indépendamment, donc les motifs répétitifs restent visibles.")
    print("• Quelles données sont restées identifiables malgré le chiffrement ?")
    print("  → Les structures géométriques, motifs réguliers, bords et zones de couleur similaires.")

def main():
    original_image_path = 'logo-linux.png'
    key = b'Sixteen byte key'  # 16 octets

    print("[*] Chargement de l'image...")
    img = Image.open(original_image_path).convert('RGB')

    print("[*] Chiffrement des pixels avec AES ECB...")
    encrypted_img = encrypt_pixels_ecb(img, key)

    print("[*] Affichage des images pour comparaison...")
    display_images(img, encrypted_img)

    afficher_reponses()

if __name__ == "__main__":
    main()
