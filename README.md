# Apprentissage par renforcement

Création d'un jeu en Python inspiré de **Geometry Dash**, puis implémentation d'un agent capable d'y jouer grâce à un **Deep Q-Network (DQN)**.

## Fichiers

Le projet est composé de plusieurs fichiers :

- **`Jeu.ipynb`** : version jouable du jeu avec affichage. Trois types d'obstacles sont implémentés : piques, carrés et plateformes.

- **`Jeu_RL`** : version sans affichage destinée à l'entraînement de l'agent.  
  L'état du jeu est représenté par 5 informations :
  - position verticale du joueur ;
  - vitesse verticale ;
  - distance au prochain obstacle ;
  - type de l'obstacle ;
  - hauteur de l'obstacle.

  Cette représentation pourrait être enrichie en donnant à l'agent davantage d'informations sur les obstacles suivants.

- **`DQN`** : implémentation de l'agent, de sa boucle d'entraînement et d'une version permettant de visualiser l'agent jouer.

- **`utils_pourRL`** : contient les fonctions et classes utiles importées par les autres fichiers.

## Principe du DQN

Le réseau reçoit l'état du jeu en entrée et estime une valeur \(Q(s,a)\) pour chaque action possible.

À chaque étape, l'agent choisit entre **exploration** et **exploitation** grâce à une stratégie ε-greedy.

Les transitions

\[
(s,a,r,s',done)
\]

sont stockées dans une **replay memory**, puis utilisées pour entraîner le réseau à respecter approximativement l'équation de Bellman :

\[
Q(s,a) \approx r + \gamma \max_{a'} Q(s',a')
\]

Un **target network**, mis à jour périodiquement, est également utilisé afin de rendre l'entraînement plus stable.

L'objectif est ainsi d'apprendre progressivement quelles actions permettent d'éviter les obstacles et d'aller le plus loin possible dans le niveau.

## Résultats