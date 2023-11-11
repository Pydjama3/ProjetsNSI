# Mastermind
Une version du jeu populaire "Mastermind" jouable dans le terminal

## Fonctionnement du jeu
### Lancement 

```shell
cd mastermind
python3 main.py
```
### Règles
Le but du jeu est de trouver une combinaison de couleurs choisies par l'ordinateur. 
Le nombre de couleurs à trouver dépend de la dificulté choisie: facile, moyen, ou difficle.  
Au lieu d'entrer les couleurs a chaque fois, vous devez entrer un chiffre entre 1 et 8. 
Chaque chiffre correspond a une couleur.      
Attention: Si vous avez déjà fait une proposition, en appuyant sur "entrée" seul, vous pouvez répéter la couleur de la dernière proposition à cet emplacement. 
Après chaque proposition, le jeu vous donnera les informations suivantes:  
- le nombre de couleurs bien placées (✅)
- le nombre de couleurs mal placées (✓)

Vous avez 12 essais pour trouver la bonne combinaison. Bonne chance !

## Librairies
- termcolor