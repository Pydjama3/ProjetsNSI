from random import randint

# Constants and global variable

color = {
  1: ['rouge', 31],
  2: ['jaune', 33],
  3: ['vert', 32],
  4: ['bleu', 34],
  5: ['mauve', 35],
  6: ['orange', 91],
  7: ['rose', 95],
  8: ['white', 37]
}
class ANSI():
    def background(code):
        return "\33[7;49;{code}m".format(code=code)

def regles():
  print("Bienvenue dans le jeu du Mastermind !")
  print("Le but du jeu est de trouver une combinaison de 4 couleurs choisies par l'ordinateur.")
  print("Chaque couleur peut prendre les valeurs : rouge, jaune, vert, bleu, mauve, orange, rose, blanc.")
  print("Vous avez 12 essais pour trouver la bonne combinaison.")
  print("Bonne chance !")

def genereCombinaison():
  """
  Cette fonction génère une combinaison de 4 chiffres choisis au hasard entre 1 et 8.
  @author Florence <3
  """
  combinaison = []
  for _ in range(4):
    combinaison.append(randint(1,8))
  return combinaison

def enterProposition():
  """
  Cette fonction demande à l'utilisateur de saisir une combinaison de 4 chiffres choisis entre
  1 et 8.
  """
  proposition = []
  for _ in range(4):
    num = input("Entrez une couleur : ")
    if len(num) == 0:
      num = int(input("Re-entrez une couleur entre 1 et 8: "))  
    while len(str(num)) > 1 or str(num).isalpha() is True:
      num = int(input("Re-entrez une couleur entre 1 et 8: "))
    num = int(num)
    while num < 1 or num > 8:
      num = int(input("Re-entrez une couleur entre 1 et 8: "))
    proposition.append(num)
  return proposition

def nbCouleurBp(combinaison, proposition):
  """
  Verfifie lesquels des nombres de couleurs sont bien placés.
  @author Florence <3
  """
  count = 0
  for i in range(4):
    if combinaison[i] == proposition[i]:
      count += 1
  return count

def nbCouleurMp(combinaison, proposition):
  """
  Cette fonction compte le nombre de couleurs mal placées.
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

  nb=sum(dResult.values())
  return nb

def jeu():
  """
  Cette fonction gère le jeu en lui même.
  """
  combinaison = genereCombinaison()
  nbEssais = 0
  gagne = False
  while nbEssais < 12:
    print(ANSI.background(color[1][1]) + str(combinaison)+"]")
    proposition = enterProposition()
    nbBp = nbCouleurBp(combinaison, proposition)
    if nbBp == 4:
      print("Vous avez gagné!!")
      gagne = True
      break
    nbMp = nbCouleurMp(combinaison, proposition) - nbBp
    print("Vous avez trouvé", nbBp, "couleurs bien placées.")
    print("Vous avez trouvé", nbMp, "couleurs mal placées.")
  if gagne is False: 
    print("Perdu!")
  

if __name__ == "__main__":
  jeu()