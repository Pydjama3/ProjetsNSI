from random import randint

from termcolor import colored  # il faut colorama pour windows (je crois)

# TODO: trouver un easter-egg (ex: pouvoir gagner le jeu en nombre
#  négatif ou null d'essais (rentrer la réponse avant le jeu)

# Constants and global variables

color = {
    # définit tous les couleurs associés à chaque nombre 
    1: "on_light_magenta",
    2: "on_red",  
    3: "on_light_red",
    4: "on_green",
    5: "on_light_green",
    6: "on_blue",
    7: "on_light_cyan",
    8: "on_cyan",
    "?": "on_black"
}

last_log = []

ESSAIS = 12

# Static asset functions
def comb_to_ui(code: list[int | str]) -> str:
    """
    Transforme une liste de nombres (références à des couleurs) en une chaine de caractères pour sortie terminal en
    couleur

    :param code: The chain of numbers representing color values
    :return: Text containing ANSI codes for coloration

    :author: Elias
    :note: Pff, j'ai pas su quoi choisir entre le RST et EpyText pour la docu -> RST est populaire et utilisé par PyCharm, RpyText supporte @author et @note...:
    """
    _colored = ""
    for character in code:
        _colored += colored(
            f"{str(character):^3s}",
            color="white" if character == "?" else "black",  # ? --> place hasn't been assigned to a value
            on_color=color[character]
        )
    return _colored


def reset_line():
    """
    "Resets" la ligne actuelle de la console

    :author: Elias
    """
    print(f"\33[2K\r", end="")
    # utlisation de codes ANSI pour éffacer la ligne (\33[2K)
    # et remettre le curseur au début (\r)


def move_up(n: int = 1):
    """
    Monter de n lignes dans la console

    :param n: le nombre de lignes qu'il faut remonter
    :author: Elias
    """
    print(f"\033[{n}A", end="")
    # utilisation du code ANSI \33[xA ou x correspond
    # au nombre de lignes dont le curseur doit remonter


def space(n: int = 1):
    """
    Permet d'aérer le texte dans le console

    :param n: le nombre de lignes à sauter

    :author: Elias
    """
    [print() for _ in range(n)]  # c'est pas beau...
    # print() --> end="\n" par défaut donc retour à la ligne


# Game Functions
def regles():
    """
    Cette fonction affiche les regles du Mastermind.

    :author: Louis, Florence
    """
    space()
    print("\x1B[4mBienvenue dans le jeu du Mastermind !\x1B[0m")
    space()
    print("Le but du jeu est de trouver une combinaison de couleurs choisies par l'ordinateur.")
    print("Le nombre de couleurs à trouver dépend de la dificulté choisie: facile, moyen, ou difficle.")
    space()
    print("Au lieu d'entrer les couleurs a chaque fois, vous devez entrer un chiffre entre 1 et 8.")
    print("Chaque chiffre correspond a une couleur:", " ; ".join([comb_to_ui([i]) for i in range(1, 9)]))
    # Pas sûr du tout des couleurs, c'est pas comme si quelqu'un allait faire attention
    # on ne va donc pas les nommer
    # (surout, c'est pas comme si quelqu'un allait lire cette docu *wink* *wink*)
    space()
    print("\t\x1b[3mSi vous avez déjà fait une proposition, en appuyant sur \"entrée\" seul,\n "
          "\tvous pouvez répéter la couleur de la dernière proposition à cet emplacement \x1b[0m")
    space()
    print("Après chaque proposition, le jeu vous donnera les informations suivantes:")
    print(" - le nombre de couleurs bien placées (\U00002705)")
    print(" - le nombre de couleurs mal placées (\U00002713)")
    space()
    print("Vous avez 12 essais pour trouver la bonne combinaison.")
    print("Bonne chance !")


def difficulte() -> int:
    """
    Cette fonction demande à l'utilisateur de choisir un niveau de difficulté.

    :return: Le niveau de difficulté renseigné par l'utilisateur

    :author: Louis
    """

    nd = ""  # là c'est du str, puis après... (voir assignations à la suite)
    while nd != "facile" and nd != "moyen" and nd != "difficile":  # "nd in <list>" serait plus simple
        nd = input("Quelle difficultée voulez vous ? (facile/moyen/difficile): ").lower()

    if nd == "facile":  # un switch serait peut être plus joli
        nd = 3  # ... c'est un int -_- heureusement qu'on est en python
    elif nd == "moyen":
        nd = 4
    else:
        nd = 5
    return nd


def genere_combinaison(nd: int = 4) -> list[int]:
    """
    Cette fonction génère une combinaison de 4 chiffres choisis au hasard entre 1 et 8.

    :param nd: la longueur de la combinaison generer
    :return: la combinaison générée aléatoirment de la longeur spécifiée

    :author: Florence
    """
    combinaison = []
    for _ in range(nd):
        combinaison.append(randint(1, 8))
    return combinaison


def entrer_proposition(nb_essai: int, nd: int = 4) -> list:
    """
    Cette fonction demande à l'utilisateur de saisir une combinaison de 4 chiffres choisis
    entre 1 et 8.

    :param nb_essai: le numero de l'essai de l'utilisateur
    :param nd: la longueur de la proposition que l'utilisateur doit entrer
    :return: les 4 propositions que l'utilisateur veut tester

    :author: Elias
    :note: C'est vraiment, mais alors vraiment pas joli tout ça
    """
    global last_log

    proposition = ["?" for _ in range(nd)]

    essai_log = f"\033[1mEssai numero {nb_essai}\033[0m"  # Beurk, le formattage et les code ANSI...
    essai_place = f"{essai_log:<23s}"  # Pour que toutes les lignes soient allignées (pas que 10, 11, et 12 décalent)

    print(f"{essai_place} - {comb_to_ui(proposition)} - ", end="")  # Début de la ligne (1x)

    for i in range(nd):  # il ya sans doute un moyen (simple) de simplifier tout ce beau monde
        num = input("Entrez une couleur: ")  # input (1x)
        while isinstance(num, int) is False:
            move_up()
            reset_line()

            try:
                num = int(num)
                if num < 1 or num > 8:
                    print(f"{essai_place} - {comb_to_ui(proposition)} - ", end="")  # (2x)
                    num = input("Re-entrez une couleur: \033[K")  # (1x)
                    continue
                else:
                    proposition[i] = num

            except ValueError:
                if num == "" and len(last_log) > 0:
                    proposition[i] = last_log[i]
                    print(f"{essai_place} - {comb_to_ui(proposition)} - ", end="")  # (3x)
                    break
                else:
                    print(f"{essai_place} - {comb_to_ui(proposition)} - ", end="")  # (4x)
                    num = input("Re-entrez une couleur: \033[K")  # (3x)
                    continue

            print(f"{essai_place} - {comb_to_ui(proposition)} - ", end="")  # (5x)

    return proposition


def nb_couleur_Bp(combinaison: list, proposition: list) -> int:
    """
    Cette fonction compte le nombre de couleurs bien placées.

    :param combinaison: la combinaison de couleur
    :param proposition: les 4 propositions que l'utilisateur veut tester
    :return: le nombre de couleurs bien placées

    :author: Florence
    """

    count = 0
    for i in range(len(combinaison)):
        if combinaison[i] == proposition[i]:
            count += 1
    return count


def nb_couleur_Mp(combinaison: list, proposition: list) -> int:
    """
    Cette fonction compte le nombre de couleurs mal placées.

    :param combinaison: la combinaison de couleur
    :param proposition: les 4 propositions que l'utilisateur veut tester
    :return: le nombre de couleurs mal placées

    :author: Louis (& Elias)
    :note: Cette fonction parait exagérément compliquée pour ce qu'elle fait mais le vendredi aprem a eu raison de moi
    """
    # Nombre d'occurences de chaque couleur dans la combinaison
    d_combinaison = {}
    for i in combinaison:
        if i in d_combinaison:
            d_combinaison[i] += 1
        else:
            d_combinaison[i] = 1

    # Nombre d'occurences de chaque couleur dans la proposiion
    d_proposition = {}
    for i in proposition:
        if i in d_proposition:
            d_proposition[i] += 1
        else:
            d_proposition[i] = 1

    # Je sais plus ce que ça fait...
    # Ah si, ça prend la plus petite valeur d'occurence de la couleur entre le combinaison et le proposition
    # (ne prend pas en compte le placement)
    # Exemple 1: proposition.jaune = 2 et combinaison.jaune = 1 --> 1 seule couleur est juste
    # Exemple 2: proposition.jaune = 1 et combinaison.jaune = 2 --> 1 seule couleur est juste
    nb = 0
    for _color in d_proposition:
        if _color in d_combinaison:
            if d_combinaison[_color] >= d_proposition[_color]:
                nb += d_proposition[_color]
            else:
                nb += d_combinaison[_color]
    return nb


def jeu():
    """
    Cette fonction gère le jeu en lui même.

    :author: Florence, Louis, et Elias
    """
    global last_log

    jouer = True  # nous rejouerons

    regles()
    space()
    nd = difficulte()
    space()

    # le choix itératif, la récurson aurait aussi pu fonctionner
    while jouer:
        last_log.clear()  # pour chaque parti il faut réinitialiser le cache
        combinaison = genere_combinaison(nd)
        gagne = False
        
        # le joueur a <ESSAI> essais
        nb_essai = 1
        for nb_essai in range(1, ESSAIS+1):
            proposition = entrer_proposition(nb_essai, nd)
            last_log = proposition  # pour le système de la dernière proposition en mémoire

            nb_bp = nb_couleur_Bp(combinaison, proposition)
            nb_mp = nb_couleur_Mp(combinaison, proposition) - nb_bp  # pour obtenir que ceux qui sont mal placés

            print(f"{nb_bp}\U00002705 et {nb_mp}\U00002713")  # \U0000<x> sont des emojis unicode

            if nb_bp == nd:
                gagne = True
                break

        space()

        # la personne a perdu: on lui montre la solution
        if not gagne:
            print(f"\033[1mVous avez perdu! La solution était: \033[0m {comb_to_ui(combinaison)} ")
            space()
            print("Retentez votre chance !")

        # la personne a gagné: on lui donne son nombre d'essais
        else:
            print("\033[1mVous avez gagné en", nb_essai, "essais!\033[0m")
            space()
            print("Vous trichez ?" if nb_essai == 1 else "Vous pouvez (sans doute) mieux faire !")

        # gagnant comme perdant on leur propose de rejouer
        if input("Voulez vous rejouez? (oui/non): ").lower() != "oui":  
          jouer = False 

        space()

if __name__ == "__main__":
    jeu()  # lancement du jeu