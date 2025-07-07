import base64

def distance_hamming(s1: bytes, s2: bytes) -> int:
    assert len(s1) == len(s2)
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(s1, s2))

def deviner_tailles_cle(texte_chiffre, taille_min=2, taille_max=40):
    distances = []
    for taille in range(taille_min, taille_max + 1):
        morceaux = [texte_chiffre[i:i+taille] for i in range(0, taille*4, taille)]
        if len(morceaux) < 4:
            continue
        paires = list(zip(morceaux, morceaux[1:]))
        moyenne = sum(distance_hamming(p[0], p[1]) for p in paires) / len(paires)
        normalise = moyenne / taille
        distances.append((taille, normalise))
    return sorted(distances, key=lambda x: x[1])

def couper_en_blocs(texte, taille):
    return [texte[i:i+taille] for i in range(0, len(texte), taille)]

def transposer_blocs(blocs, taille):
    transposes = [b'' for _ in range(taille)]
    for bloc in blocs:
        for i in range(len(bloc)):
            transposes[i] += bytes([bloc[i]])
    return transposes

def xor_simple(texte: bytes, cle: int) -> bytes:
    return bytes([b ^ cle for b in texte])

def score_texte(texte: bytes) -> float:
    frequences = {
        'a': 0.065, 'b': 0.012, 'c': 0.021, 'd': 0.034,
        'e': 0.104, 'f': 0.019, 'g': 0.016, 'h': 0.049,
        'i': 0.055, 'j': 0.001, 'k': 0.005, 'l': 0.033,
        'm': 0.020, 'n': 0.056, 'o': 0.059, 'p': 0.013,
        'q': 0.001, 'r': 0.049, 's': 0.051, 't': 0.072,
        'u': 0.022, 'v': 0.008, 'w': 0.017, 'x': 0.001,
        'y': 0.014, 'z': 0.001, ' ': 0.19
    }
    return sum(frequences.get(chr(b).lower(), 0) for b in texte)

def meilleur_octet_cle(bloc: bytes) -> int:
    scores = []
    for cle_candidate in range(256):
        xored = xor_simple(bloc, cle_candidate)
        score = score_texte(xored)
        scores.append((cle_candidate, score))
    return max(scores, key=lambda x: x[1])[0]

def dechiffrer_xor_cle_repetee(texte_chiffre):
    tailles_cle = deviner_tailles_cle(texte_chiffre)[:3]
    resultats = []
    for taille, _ in tailles_cle:
        blocs = couper_en_blocs(texte_chiffre, taille)
        transposes = transposer_blocs(blocs, taille)
        cle = bytes([meilleur_octet_cle(bloc) for bloc in transposes])
        texte_dechiffre = bytes([b ^ cle[i % len(cle)] for i, b in enumerate(texte_chiffre)])
        resultats.append((cle, texte_dechiffre))
    return resultats

def main():
    with open("6.txt", "r") as f:
        donnees_b64 = f.read()
    texte_chiffre = base64.b64decode(donnees_b64)
    resultats = dechiffrer_xor_cle_repetee(texte_chiffre)
    for cle, texte in resultats:
        print("="*40)
        print(f"Clé trouvée : {cle}")
        print("-"*40)
        print(texte.decode("utf-8", errors="replace"))
        print("="*40)

if __name__ == "__main__":
    main()