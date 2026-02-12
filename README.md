# Hexmaster2

## Faction  
Une faction est un ensemble de créatures, bâtiments et cases.

## Statistiques
Vie (PV), point de vie d'une entité
Combat (Co), les dégats infligés aux créatures
Démolition (DM), les dégats infligés aux bâtiments
Dégradation (DG), les dégats infligés aux cases
Portée (Po), distance à laquelle on peut attaquer
Mouvement (Mo), permet de se déplacer sur la carte
Compétences (Comp), des effets divers et variés

## Créature
- se déplacer
- infliger des dégats aux créature et bâtiments
- bloquer l'accès à une case
- exercer du contrôle sur une case

## Bâtiment
- infliger des dégats aux créatures, bâtiments et cases
- bloquer l'accès à une case
- exercer du contrôle sur une case

## Case
- infliger des dégats aux créatures et bâtiments
- permettre l'apparition d'unités et bâtiments

## Mode de jeu

### Classique
Tuer tout les ennemis ou obtenir le contrôle d'une proportion de cases

### Contrôle de points
Tuer tout les ennemis ou obtenir le contrôle de certaines cases spécifiques

### Combat à mort
Tuer tout les ennemis

### Défense de bâtiment
Protéger lesdits bâtiment, si l'un casse, alors la partie est perdue, pour gagner, survivre aux différentes vagues d'ennemis

## Gameplay général
Tour par tour
Une ressource nommé "Inv", qui permet d'invoquer
Un kill rapporte des Points d'Inv (PI)
Le contrôle de case rapporte des PI

### Gestion d'un tour
1. Le joueur gagne X PI (valeur à déterminer)  
2. Le joueur peut placer des cartes / jouer des entites  
3. Le joueur déclare la fin du tour  

## Créer un environnement virtuel
On commence par générer un environnement virtuel avec la commande  
python3 -m venv .venv  

Ensuite on l'active  
source .venv/bin/activate  

Puis on installe les librairies  
pip install -r requirements.txt  

## Lancer le jeu avec python

Pour lancer le jeu avec python, on traite le jeu comme une bibliothèque, il faut donc utiliser :  
python -m src.main [mode]  
mode: [playground / demo]  

## Lancer les tests
Tests de fonctions :  
python3 -m unittest discover  

Coverage :  
pytest --cov=src  

Pour Coverage avec le détail des lignes non exécutées :  
pytest --cov=src --cov-report=term-missing  
