# Apprentissage-renfo
Création d'un jeu en python et implémentation d'une IA RL

## Fichier

Le projet est composé de plusieurs fichier:

- le premier est le dossier Jeu.ipynb qui implémente un jeu GeometryDash-like jouable avec le clavier, il 
n'y a que trois classes d'objets: pique où tout contact fait perdre le joueur, carré où le joueur peut se poser 
dessus mais un contact sur les bords implique la mort du joueur, et plateforme à travers laquelle le joueur peut passer et sur laquelle il peut se poser. Ce premier fichier met également en place la classe affichage qui sera plaisante pour visionner notre agent qui joue

- le deuxième fichier Jeu_RL est une version du jeu sans affichage destinée à être la version
sur laquelle l'agent s'entraîne (afficher le jeu ralentirait énormément l'entrainement). Cette version du jeu est complétée par "get_state" qui permet d'obtenir l'état actuel du jeu que j'ai limité à 5 éléments dans un premier temps: vitesse verticale du joueur, position verticale, distance au prochain obstacle, type du prochain obstacle et hauteur du prochain obstacle, on a evidemment une large marge de manoeuvre pour améliorer notre agent: on aurait pu rajoute la vitesse horizontale, la taille des objets, et une vision à deux ou trois objets, pas juste le suivant. Cette version du jeu est aussi constituée d'un reset qui permettra aà l'agent de recommencer

- Enfin, DQN, le troisième fichier, met en place l'agent, sa boucle d'entrainement ainsi qu'une version du jeu où c'est l'agent lui même qui joue. 

- Le fichier qui fait le pont entre tous les autres fichiers est utils_pourRL qui est constitué de copies des fonctions utiles de Jeu_RL que j'importe dans DQN.

## Principe du DQN

