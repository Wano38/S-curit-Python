import base64
from Crypto.Cipher import AES



def lire_lignes_hex(fichier):
    with open(fichier, 'r') as f:
        return [ligne.strip() for ligne in f]


def hex_vers_blocs(hex_str):
    donnees = bytes.fromhex(hex_str)
    return [donnees[i:i+16] for i in range(0, len(donnees), 16)]


def compter_blocs_repetes(blocs):
    return len(blocs) - len(set(blocs))

def trouver_ecb(lignes):
    max_repetitions = 0
    ligne_ecb = ''
    index_ligne = -1

    for i, ligne in enumerate(lignes):
        blocs = hex_vers_blocs(ligne)
        repetitions = compter_blocs_repetes(blocs)

        if repetitions > max_repetitions:
            max_repetitions = repetitions
            ligne_ecb = ligne
            index_ligne = i + 1  # lignes commencent à 1

    return index_ligne, ligne_ecb


def main():
    lignes = lire_lignes_hex("Chal8.txt")
    index, texte = trouver_ecb(lignes)
    print(f"ECB détecté à la ligne {index} :\n{texte}")



if __name__ == "__main__":
    main()
