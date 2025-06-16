
import itertools
import time

c = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
mot = 'Caca2'

def test(mot, f):
    if mot == f:
        print('MDP déchiffré:', f)
        return True
    return False

def charger_dictionnaire(nom_fichier):
    with open(nom_fichier, 'r', encoding='utf-8') as fichier:
        return [ligne.strip() for ligne in fichier]

def bruteforce_s():
    longueur = 1
    start_time = time.time()  # Début du chronométrage
    while True:
        for i in itertools.product(c, repeat=longueur):
            f = ''.join(i)
            print(f)  
            if test(mot, f):
                end_time = time.time()  # Fin du chronométrage
                elapsed_time = end_time - start_time
                print(f'Temps pris (bruteforce_s) : {elapsed_time:.2f} secondes')
                return
        longueur += 1
        
def bruteforce_d(dictionnaire):
    start_time = time.time()  # Début du chronométrage
    for f in dictionnaire:
        print('Essai:', f)
        if test(mot, f):
            end_time = time.time()  # Fin du chronométrage
            elapsed_time = end_time - start_time
            print(f'Temps pris (bruteforce_d) : {elapsed_time:.2f} secondes')
            return True
    bruteforce_s()
        
nom_fichier = r'dico_mini_fr.txt'
dictionnaire = charger_dictionnaire(nom_fichier)
bruteforce_d(dictionnaire)
# bruteforce_s()
