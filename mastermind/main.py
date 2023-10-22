from random import randint

# Constants and global variable

color = {
    1: ['rouge', 41],
    2: ['jaune', 93],
    3: ['vert', 42],
    4: ['bleu', 44],
    5: ['mauve', 45],
    6: ['orange', 2],
    7: ['rose', 46],
    8: ['blanc', 47]
}

class PrintColours:

  def __init__(self, string) -> None:
    assert isinstance(string, str)

    self.string = string
    self.bg_color = 0
    self.style = 0
    self.tx_color = 0

  def style_text(self, code):
    self.style = code
    return self

  def color_text(self, code):
    self.tx_color = code
    return self

  def background(self, code):
    self.bg_color = code
    return self

  def __str__(self) -> str:
    #return f"\33[{self.bg_color}m\33[{self.tx_color}m\33[{self.style}m" + self.string + "\33[0m"
    return f"\33[{self.bg_color}m" + self.string + "\33[0m"

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
      #printColours(combinaison)
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

def indexToANSI(t, bg=0, st=0, co=0):
  ansi = PrintColours(t).background(bg).color_text(co).style_text(st)
  return str(ansi)

def printColours(colourList):
  colourful = [indexToANSI(str(e), bg=color[e][1]) for e in colourList]
  print(indexToANSI("1", bg=1))

if __name__ == "__main__":
  jeu()
