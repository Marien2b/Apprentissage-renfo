import copy 

class Objet:
    def __init__(self, x, y):
        self.x = x
        self.y = y 


class Joueur(Objet):
    def __init__(self, x, y, vy, vx):
        super().__init__(x,y)
        self.vy = vy
        self.vx = vx
        self.gravite = -0.9

class carre(Objet):
    def __init__(self, x, y, taille):
        super().__init__(x,y)
        self.taille = taille

class plateforme(Objet):
    def __init__(self, x, y):
        super().__init__(x,y)
    

class pique(Objet):
    def __init__(self, x, y, taille):
        super().__init__(x,y)
        self.taille = taille

class Jeu:
    def __init__(self):
        self.joueur = Joueur(0, 0, 0, 6.5)
        self.obstacles = []
        self.obstacles_bis = []
        self.score = 0

    def ajouter_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
        self.obstacles_bis.append(copy.deepcopy(obstacle))

    def saut(self):
        if self.joueur.y == 0 or self.surplateform(self.joueur.x, self.joueur.y):
            self.joueur.vy = 15
        

    def deplacer_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.x -= self.joueur.vx

    def surplateform(self, x, y):
        for obstacle in self.obstacles:
            if isinstance(obstacle, plateforme):
                largeur = 150
                hauteur_support = obstacle.y
            elif isinstance(obstacle, carre):
                largeur = obstacle.taille
                hauteur_support = obstacle.y + obstacle.taille
            else:
                continue

            chevauchement = x + 50 > obstacle.x and x < obstacle.x + largeur
            if chevauchement and abs(y - hauteur_support) < 1:
                return True
        return False

    def plateforme_traversee(self, y_avant, y_apres):
        for obstacle in self.obstacles:
            if isinstance(obstacle, plateforme):
                largeur = 150
                hauteur_support = obstacle.y
            elif isinstance(obstacle, carre):
                largeur = obstacle.taille
                hauteur_support = obstacle.y + obstacle.taille
            else:
                continue
            chevauchement = (
                self.joueur.x + 50 > obstacle.x
                and self.joueur.x < obstacle.x + largeur
            )
            if chevauchement and y_avant >= hauteur_support >= y_apres:
                return hauteur_support
        return None
        
    def mettre_a_jour_joueur(self):
        y_avant = self.joueur.y
        self.joueur.vy += self.joueur.gravite
        y_apres = y_avant + self.joueur.vy

        hauteur_touchee = None
        if self.joueur.vy <= 0:
            hauteur_touchee = self.plateforme_traversee(y_avant, y_apres)

        if hauteur_touchee is not None:
            self.joueur.y = hauteur_touchee
            self.joueur.vy = 0
        elif y_apres <= 0:
            self.joueur.y = 0
            self.joueur.vy = 0
        else:
            self.joueur.y = y_apres

    def mettre_a_jour_score(self):
        self.score += 1

        if self.score % 10 == 0:
            self.joueur.vx += 0.01

    def verifier_collision(self):
        for obstacle in self.obstacles:

            if isinstance(obstacle, plateforme):
                
                continue  

            else:
                if isinstance(obstacle, carre):
                    chevauchement_x = (
                        self.joueur.x + 50 >= obstacle.x
                        and self.joueur.x <= obstacle.x + obstacle.taille
                    )
                    chevauchement_y = (
                        self.joueur.y + 50 >= obstacle.y
                        and self.joueur.y <= obstacle.y + obstacle.taille
                    )
                    vraiment_sur_le_dessus = (
                        self.joueur.x + 50 > obstacle.x
                        and self.joueur.x < obstacle.x + obstacle.taille
                        and abs(self.joueur.y - (obstacle.y + obstacle.taille)) < 1
                    )
                    if chevauchement_x and chevauchement_y and not vraiment_sur_le_dessus:
                        return True
                if isinstance(obstacle, pique):
                    gauche = max(self.joueur.x, obstacle.x)
                    droite = min(self.joueur.x + 50, obstacle.x + obstacle.taille)

                    if gauche > droite:
                        continue
                    sommet_x = obstacle.x + obstacle.taille / 2
                    X = min(max(sommet_x, gauche), droite)

                    # Hauteur du pique en X
                    hauteur_pique = (
                        obstacle.y
                        + obstacle.taille
                        - 2 * abs(X - sommet_x)
                                )

                    if (
                        self.joueur.y <= hauteur_pique
                    and self.joueur.y + 50 >= obstacle.y
                    ):
                        return True
                    else:
                        continue

                

        return False

    def get_state(self):
        typobs = -1
        for obstacle in self.obstacles:
            if obstacle.x - self.joueur.x > 0:
                dist = obstacle.x - self.joueur.x
                obsy = obstacle.y
                if isinstance(obstacle, pique):
                    typobs = 0
                elif isinstance(obstacle, carre):
                    typobs = 1
                elif isinstance(obstacle, plateforme):
                    typobs = 2
                break
        if typobs == -1:
            return 0
        

            

        return self.joueur.y, self.joueur.vy, dist, typobs, obsy

    def step(self, action):
        reward = 1
        done = False
        if action == 1:
            self.saut()
        self.deplacer_obstacles()
        self.mettre_a_jour_joueur()
        self.mettre_a_jour_score()

        if self.verifier_collision():
            reward -= 100
            done = True
        next_state = self.get_state()
        if next_state == 0:
            reward = 100
            done = True
        return next_state, reward, done

    def reset(self):
        self.joueur = Joueur(0, 0, 0, 6.5)
        self.score = 0
        self.obstacles = copy.deepcopy(self.obstacles_bis)
        return self.get_state()

jeu = Jeu()

def niveau1(jeu):

    # Début tranquille
    jeu.ajouter_obstacle(pique(500, 0, 40))
    jeu.ajouter_obstacle(pique(750, 0, 40))

    # Petit enchaînement
    jeu.ajouter_obstacle(pique(950, 0, 40))
    jeu.ajouter_obstacle(pique(1000, 0, 40))

    # Première plateforme
    jeu.ajouter_obstacle(plateforme(1250, 100))
    jeu.ajouter_obstacle(pique(1250, 0, 50))
    jeu.ajouter_obstacle(pique(1300, 0, 50))
    jeu.ajouter_obstacle(pique(1350, 0, 50))

    # Obstacle après la plateforme
    jeu.ajouter_obstacle(pique(1750, 0, 40))

    # Partie un peu plus verticale
    jeu.ajouter_obstacle(plateforme(1950, 80))
    jeu.ajouter_obstacle(plateforme(2200, 150))

    # Retour au sol
    jeu.ajouter_obstacle(pique(2500, 0, 40))
    jeu.ajouter_obstacle(pique(2550, 0, 40))

    # Petit final
    jeu.ajouter_obstacle(pique(2800, 0, 50))
    jeu.ajouter_obstacle(pique(3000, 0, 40))
    jeu.ajouter_obstacle(pique(3300, 0, 40))

def niveau2(jeu):
    """Niveau intermédiaire: alternance de pointes, escaliers de plateformes
    et sections de carrés (obstacles imposants)."""
    # Alternance de pointes pour commencer
    jeu.ajouter_obstacle(pique(500, 0, 40))
    jeu.ajouter_obstacle(pique(650, 0, 40))

    # Petit obstacle isolé
    jeu.ajouter_obstacle(pique(900, 0, 50))

    # Plateformes en escalier (hauteurs variées)
    x = 1150
    for h in (40, 80, 120, 160, 120, 80):
        jeu.ajouter_obstacle(plateforme(x, h))
        x += 220

    # Couloir avec gros carrés rapprochés (forcer à sauter précisément)
    jeu.ajouter_obstacle(carre(2800, 0, 60))
    jeu.ajouter_obstacle(carre(2850, 0, 40))

    # Petits pointes avant le final
    jeu.ajouter_obstacle(pique(3100, 0, 50))
    jeu.ajouter_obstacle(pique(3150, 0, 50))

    # Final: séries de plateformes décalées
    jeu.ajouter_obstacle(plateforme(3400, 150))
    jeu.ajouter_obstacle(plateforme(3650, 100))
    jeu.ajouter_obstacle(plateforme(3850, 60))

def niveau3(jeu):
    """Niveau difficile: ridges de pointes, alternance haute/basse, tours
    de carrés et longue crête finale de pointes."""
    # Début agressif
    jeu.ajouter_obstacle(pique(500, 0, 60))
    jeu.ajouter_obstacle(pique(580, 0, 60))

    # Plateforme haute à atteindre
    jeu.ajouter_obstacle(plateforme(750, 200))
    jeu.ajouter_obstacle(pique(800, 0, 50))

    # Ridge de pointes de tailles variées
    for i, s in enumerate((60, 40, 80, 40, 60)):
        jeu.ajouter_obstacle(pique(950 + i * 90, 0, s))

    # Alternance haute/basse de plateformes rapprochées
    x = 1400
    for i in range(6):
        jeu.ajouter_obstacle(plateforme(x, 150 if i % 2 == 0 else 60))
        # petites pointes sur certaines plateformes
        if i % 2 == 0:
            jeu.ajouter_obstacle(pique(x + 80, 0, 40))
        x += 220

    # Tours/obstacles empilés (carres) pour forcer trajectoires
    jeu.ajouter_obstacle(carre(2800, 0, 80))
    jeu.ajouter_obstacle(carre(2950, 80, 60))
    jeu.ajouter_obstacle(plateforme(3150, 180))

    # Longue crête finale de pointes
    for i in range(10):
        jeu.ajouter_obstacle(pique(3400 + i * 60, 0, 40))


# Par défaut, on garde l'appel à niveau1 pour compatibilité
niveau1(jeu)


