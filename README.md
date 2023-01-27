Projet Poly#
============

Le projet polyhash est un projet de programmation réalisé dans le cadre du module "projet de developpement logiciel", inspiré du [google hashcode](https://codingcompetitions.withgoogle.com/hashcode/round/00000000008cacc6)

L'équipe
========
nous somme l'équipe IDIA B composés de :

## Othman IBRHIMI (ibrahimi.othman.2000@gmail.com)
responsable visualisation

## Maxime DANIEL (maxime.daniel208@gmail.com)
responsable modele et données
## Childéric OLIET (oliet.childéric@gmail.com)
responsable sérialisation et stratégie boucle

## Juan David RAMIREZ (jdramirezo@unal.edu.co)
responsable stratégie déplacement point a point et boucle


Installation des dépendances
========================
installez les dépendances suivantes via pip: `pip install scipy tkinter`
une installation récente de python (3.10.7) est fortement recommandée

Execution
========================

pour lancer le projet, faites la commande  `python3 polyhash.py` dans le répertoire courrant, puis entrez le nom du fichier d'entrée (chemin relatif)
le fichier de solution sera automatiquement sorti comme test.out.py
une trace d'execution sera aussi imprimée dans le terminal, et finalement la dernière ligne indiquera le score final calculé

stratégies
========================
il y a trois niveau de stratégie différente sur lequel l'on a travaillé
## stratégie de stockage des données
l'on s'est très vite rendu compte que la manière dont les données serait stockées aurait un impact majeur sur les performances mémoires et temporelles de l'application, c'est donc pourquoi l'on a très vite décidé d'une structure pour stocker efficacement les données:
### Cadeau:
> le cadeau est l'unité "de base" de la structure de données, c'est une classe contenant toute les informations jugées nécéssaires sur un cadeau, ainsi que deux booléens "delivre" et "enTransport" qui sont exploités par les algos de résolution de chemin pour isoler les **cadeaux** déja gérés
### Groupe:
> un groupe symbolise une coordonnée X,Y dans le tableau, il est possible a partir de cette coordonnée là d'accéder a un certain nombre de **cadeaux**, on peut donc faire un "dépot groupé" sur ce point. Un groupe est représenté par une classe, il puise ses informations (poids, score) directement des **cadeaux**.
### Région:
> une région est un ensemble de **groupes** situés dans un carré d'une certaine taille,cela permet de dynamiquement charger ou non seul une partie du problème, pour ne pas faire de dépassement mémoire

cette solution nous a permis d'avoir un moyen de récuperer les infos de manière rapide et sans consommer trop de mémoire
## stratégie de déplacement point a point
L'on a décidé de structurer nos déplacement de telle manière que l'unité minimale d'un déplacement serait un "chemin", ce **chemin** amène le traineau du pere noel d'un **groupe** a un autre. Par manque de temps, il n'est pas possible de transferer la vélocité d'un parcours a un autre (l'on démare et fini toujours un **chemin** avec 0 de vitesse), ce qui a sans doute contribué a notre bas score, si plus de temps nous avait été accordé cela aurait été l'un des sujets a plus haute priorité.
### pré-estimation du parcours
avant meme de générer le parcours, il peut etre evalué, en effet avec l'aide de beaucoup de math (expliqués en détail dans le code), il est possible de prévoir le cout en carrotes et en temps d'un parcours avant de générer la suite d'instructions exactes, cela accelere grandement la vitesse d'execution du programme dans des cas de longues distances.
### génération du parcours
le parcours se fait actuellement sous une forme de "L", dans un premier temps, on accélere dans la coordonée X, puis on ralenti pour arriver exactement aux bonne coordonées X, rebelote pour la coordonée Y et nous arrivons a destination (les détails d'implémantation sont commentés dans le code), avec plus de temps nous aurions ésperer pouvoir combiner les acceleration dans les coordonées X et Y pour pouvoir gagner un peu de temps, mais trouver un algorythme efficace s'avéra difficile.

## stratégie de boucles
une fois que l'on a nos chemins, on les assembles dans des "boucles" commençant en 0,0 par un chargement de cadeaux et carrotes, puis finissant en 0,0. Pour généer ce parcours, l'on aurait aimé developper un algorithme efficace (peut etre en utilisant des parcours de graphes ou du A*), mais nous n'avons rien pu finir a temps, donc actuellement c'est une simple recherche du plus proche, meilleur score et moins lourd, il y a cependant un morceau de stratégie interresante pour faire que les boucles soient intactes.
### création de boucles
pour créer une boucle, on commence en 0,0 puis on ajoute le procain cadeau a la boucle, on fait le chemin du cadeau a 0,0 puis celui de 0,0 vers le cadeau (qui a besoin du poids du parcours suivant, car devra porter les cadeaux/Carottes), ensuite lors de l'ajout d'un deuxième cadeau l'on fait d'abbord le chemin cadeau 2 -> cadeau 1, puis 0,0 -> cadeau 2 etc...

organisation du code
========================
le gros du code est organisé sous la forme de classes dans la partie model, ensuite il existe deux fonctions annexes "scorer" et "fileParser" qui permettent respectivement de donner un score a une solution et de lire les fichiers problemes.
Optimalement l'algorithme de résolution aurait été intégré au projet de manière plus propre, c'est actuellement un simple script de test de stratégie, je détaillerai dans la partie suivante plus les raisons

bugs et limitations connu.e.s
========================
## algorithme non optimisé
l'algorithme s'occupant du parcours final n'est absolument pas optimisé, la stratégie actuelle est très basique car nous n'avons pas pu avancer assez dans ce secteur, ainsi l'algorithme de résolution utilisé dans la version finale n'est qu'une version "de test" de base destinée a juger le bon fonctionnement ou non des autres parties du code et non un algo complet et efficace. ainsi les problèmes E et F ne sont pas résolu asez bien par l'algo actuel incapable de concevoir des parcours adaptés

## impossible de résoudre le problème B
malgré tout nos efforts, il nous est impossible de déposer un singulier cadeau pour le problème B, car notre algo de déplacement de point a point actuel utilise une acceleration puis un ralentissement, utilisant trop de ressources pour les demandes du probleme B
