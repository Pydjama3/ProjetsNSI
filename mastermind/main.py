from random import randint

from termcolor import colored, cprint, COLORS, HIGHLIGHTS

# Constants and global variables

color = {i:list(HIGHLIGHTS.keys())[i+2] for i in range(1, 9)}

# Static functions
def comb_to_ui(code):
  _colored = ""
  for character in code:
    _colored += colored(f"{str(character):^3s}", "black", color[int(character)])
  return _colored

# Functions
def regles():
  """ 
  Cette fonction affiche les regles du Mastermind.
  """
  print("Bienvenue dans le jeu du Mastermind !")
  print("Le but du jeu est de trouver une combinaison de 4 couleurs choisies par l'ordinateur.")
  print("Chaque couleur peut prendre les valeurs : rouge, jaune, vert, bleu, mauve, orange, rose, blanc.")
  print("Au lieu d'entrer les couleurs a chaque fois, vous devez entrer un chiffre entre 1 et 8.")
  print("Chaque chiffre correspond a une couleur.")
  print("Vous avez 12 essais pour trouver la bonne combinaison.")
  print("Bonne chance !")

def difficulte():
  '''
  Cette fonction demande à l'utilisateur de choisir un niveau de difficulté.
  Returns:
    nd (int) : le numero correspondant à la difficultée (facile = 3, moyen = 4, difficile = 5)
  '''
  nd = ""
  while nd != "facile" and nd != "moyen" and nd != "difficile":
    nd = input("\nQuelle difficultée voulez vous ? (facile/moyen/difficile) : ").lower()
  if nd == "facile":
    nd = 3
  elif nd == "moyen":
    nd = 4
  else:
    nd = 5
  return nd

def genere_combinaison(nd=4):
  """
  Cette fonction génère une combinaison de 4 chiffres choisis au hasard entre 1 et 8.
  Paramètre:
    nd (int) : la longueur de la combinaison generer
  Returns: 
    combinaison (list) : la combinaison de couleur de longueur nd
  """
  combinaison = []
  for _ in range(nd):
    combinaison.append(randint(1, 8))
  return combinaison

def entrer_proposition(nbEssai, nd=4):
  """
  Cette fonction demande à l'utilisateur de saisir une combinaison de 4 chiffres choisis
  entre 1 et 8.
  Paramètre:
    nbEssai (int) : le numero de l'essai de l'utilisateur
    nd (int) : la longueur de la proposition que l'utilisateur doit entrer
  Returns:
    proposition (list) : les 4 propositions que l'utilisateur veut tester
  """
  proposition = []
  print("\n\033[1mEssai numero", nbEssai+1,"\033[0m")
  for _ in range(nd):
    num = input("Entrez une couleur : ")
    while isinstance(num, int) is False:
      try:
        num = int(num)
        if num < 1 or num > 8:
          num = input("\033[1ARe-entrez une couleur : \033[K")
          continue
      except ValueError:
        num = input("\033[1ARe-entrez une couleur : \033[K")
        continue
    proposition.append(num)
  return proposition

def nb_couleur_Bp(combinaison, proposition):
  """
  Cette fonction compte le nombre de couleurs bien placées.
  Paramètres:
    combinaison (list) : la combinaison de couleur
    proposition (list) : les 4 propositions que l'utilisateur veut tester
  Returns:
    count (int) : le nombre de couleurs bien placées 
  """
  count = 0
  for i in range(len(combinaison)):
    if combinaison[i] == proposition[i]:
      count += 1
  return count

def nb_couleur_Mp(combinaison, proposition):
  """
  Cette fonction compte le nombre de couleurs mal placées.
  Paramètres:
    combinaison (list) : la combinaison de couleur
    proposition (list) : les 4 propositions que l'utilisateur veut tester
  Returns:
    nb (int) : le nombre de couleurs mal placées 
  """
  nb = 0
  dCombinaison = {}
  for i in combinaison:
    if i in dCombinaison:
      dCombinaison[i] += 1
    else:
      dCombinaison[i] = 1

  dProposition = {}
  for i in proposition:
    if i in dProposition:
      dProposition[i] += 1
    else:
      dProposition[i] = 1

  dResult = {}
  for color in dProposition:
    if color in dCombinaison:
      if dCombinaison[color] >= dProposition[color]:
        dResult[color] = dProposition[color]
      else:
        dResult[color] = dCombinaison[color]

  nb = sum(dResult.values())
  return nb

def jeu():
  """
  Cette fonction gère le jeu en lui même.
  """
  jouer = True
  regles()
  nd = difficulte()
  while jouer:
    combinaison = genere_combinaison(nd)
    gagne = False
    for nbEssai in range(12):
      print(comb_to_ui(combinaison))
      proposition = entrer_proposition(nbEssai, nd)
      nbBp = nb_couleur_Bp(combinaison, proposition)
      if nbBp == nd:
        print("\n\033[1mVous avez gagné en", nbEssai+1, "essais!\033[0m")
        gagne = True
        break
      nbMp = nb_couleur_Mp(combinaison, proposition) - nbBp
      print("Vous avez trouvé", nbBp, "couleurs bien placées.")
      print("Vous avez trouvé", nbMp, "couleurs mal placées.")
    if not gagne:
      print("\n\033[1mVous avez perdu!\033[0m")
    if input("Voulez vous rejouez? (oui/non) : ").lower() == "non":
      jouer = False

if __name__ == "__main__":
  jeu()
