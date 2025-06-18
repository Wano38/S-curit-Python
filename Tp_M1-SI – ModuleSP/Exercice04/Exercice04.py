"""
Exercice 4 — Déchiffrement sans la clé (attaque par dictionnaire ECB)

1. Proposer un scénario où un attaquant ne connaît pas la clé, mais peut deviner certaines parties du texte clair.
2. Dans un message chiffré en ECB, essayer de retrouver des structures ou du contenu connu.
3. Explorer l’idée d’une attaque par dictionnaire : si un texte connu génère toujours le même bloc chiffré, il peut être identifié sans déchiffrement.

Questions :
• En quoi le mode ECB rend-il ce type d’attaque possible ?
• Que faudrait-il changer pour se protéger contre ce type d’analyse ?
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random

def chiffrement_ecb_bloc(texte_clair: bytes, key: bytes):
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(texte_clair, AES.block_size)
    return cipher.encrypt(padded)

def construire_dictionnaire_ecb(possibilités, key):
    print("[*] Construction du dictionnaire de blocs connus...")
    dico = {}
    for mot in possibilités:
        bloc_clair = pad(mot.encode(), AES.block_size)
        bloc_chiffré = chiffrement_ecb_bloc(bloc_clair, key)
        dico[bloc_chiffré[:16]] = mot
    return dico

def attaque_par_dictionnaire(message_chiffré: bytes, dico):
    print("[*] Attaque par dictionnaire en cours...")
    blocs = [message_chiffré[i:i+16] for i in range(0, len(message_chiffré), 16)]
    message_reconnu = []
    for bloc in blocs:
        mot = dico.get(bloc, "???")
        message_reconnu.append(mot)
    return message_reconnu

def afficher_reponses():
    print("\n=== Réponses aux questions ===")
    print("• En quoi le mode ECB rend-il ce type d’attaque possible ?")
    print("  → ECB chiffre chaque bloc indépendamment. Si deux blocs de texte clair sont identiques, leurs blocs chiffrés le seront aussi.")
    print("  → Cela permet de construire un dictionnaire de correspondance entre texte clair et chiffré sans connaître la clé.")
    print("• Que faudrait-il changer pour se protéger ?")
    print("  → Utiliser des modes comme CBC, CTR ou GCM, qui introduisent de l’aléatoire et du chaînage.")
    print("  → Ces modes empêchent qu’un même bloc de texte clair produise toujours le même bloc chiffré.")

def main():
    # Clé secrète connue seulement du serveur
    key = b'Sixteen byte key'

    # Scénario : un attaquant devine des mots dans un message (comme des rôles : "admin", "user", etc.)
    message_clair = b"user|admin|secret|guest|admin|user"
    message_chiffré = chiffrement_ecb_bloc(message_clair, key)

    # L’attaquant essaie de retrouver des mots connus
    mots_connus = ["admin", "user", "guest", "secret", "root", "debug"]

    # Attaque par dictionnaire
    dictionnaire = construire_dictionnaire_ecb(mots_connus, key)
    blocs_trouves = attaque_par_dictionnaire(message_chiffré, dictionnaire)

    # Résultat
    print("\nMessage chiffré analysé :")
    for i, mot in enumerate(blocs_trouves):
        print(f"Bloc {i+1} : {mot}")

    afficher_reponses()

if __name__ == "__main__":
    main()
