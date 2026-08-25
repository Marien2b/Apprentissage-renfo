import copy 
import pygame


def type_obstacle(obstacle):
    """Renvoie un type stable meme apres un reload dans Jupyter."""
    return type(obstacle).__name__.lower()


def largeur_obstacle(obstacle):
    if type_obstacle(obstacle) == "plateforme":
        return 150
    return obstacle.taille

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
            if type_obstacle(obstacle) == "plateforme":
                largeur = 150
                hauteur_support = obstacle.y
            elif type_obstacle(obstacle) == "carre":
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
            if type_obstacle(obstacle) == "plateforme":
                largeur = 150
                hauteur_support = obstacle.y
            elif type_obstacle(obstacle) == "carre":
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

            if type_obstacle(obstacle) == "plateforme":
                
                continue  

            else:
                if type_obstacle(obstacle) == "carre":
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
                if type_obstacle(obstacle) == "pique":
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
        # Garder une forme constante (5 valeurs) est indispensable pour le DQN,
        # y compris pendant la derniere transition d'un episode.
        prochain_obstacle = None
        for obstacle in self.obstacles:
            largeur = largeur_obstacle(obstacle)
            # L'obstacle reste pertinent jusqu'a ce qu'il soit entierement passe.
            if obstacle.x + largeur > self.joueur.x:
                prochain_obstacle = obstacle
                break

        if prochain_obstacle is None:
            return self.joueur.y, self.joueur.vy, 0.0, -1, 0.0

        if type_obstacle(prochain_obstacle) == "pique":
            type_obstacle_id = 0
        elif type_obstacle(prochain_obstacle) == "carre":
            type_obstacle_id = 1
        else:
            type_obstacle_id = 2

        distance = prochain_obstacle.x - self.joueur.x
        return (
            self.joueur.y,
            self.joueur.vy,
            distance,
            type_obstacle_id,
            prochain_obstacle.y,
        )

    def step(self, action):
        reward = 1
        done = False
        if action == 1:
            self.saut()
        self.deplacer_obstacles()
        self.mettre_a_jour_joueur()
        self.mettre_a_jour_score()

        collision = self.verifier_collision()
        if collision:
            reward -= 100
            done = True
        next_state = self.get_state()
        if not collision and next_state[3] == -1:
            reward = 100
            done = True
        return next_state, reward, done

    def reset(self):
        self.joueur = Joueur(0, 0, 0, 6.5)
        self.score = 0
        self.obstacles = copy.deepcopy(self.obstacles_bis)
        return self.get_state()

class Affichage:
    def __init__(self, jeu):
        self.jeu = jeu

        pygame.init()
        self.ecran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("GD Test")


    def dessiner_obstacle(self, obstacle):
        # Les notebooks peuvent conserver des instances d'une ancienne version
        # des classes apres la reexecution d'une cellule. Le nom de classe reste
        # stable et evite alors que tous les obstacles deviennent invisibles.
        nom_type_obstacle = type(obstacle).__name__.lower()

        if nom_type_obstacle == "carre":
            pygame.draw.rect(
                self.ecran,
                pygame.Color("red"),
                pygame.Rect(
                    obstacle.x,
                    600 - obstacle.y - obstacle.taille,
                    obstacle.taille,
                    obstacle.taille
                )
            )
            

        elif nom_type_obstacle == "plateforme":
            largeur = 150
            hauteur = 20

            x = obstacle.x
            y = 600 - obstacle.y

            pygame.draw.rect(
                self.ecran,
                pygame.Color("green"),
                pygame.Rect(
                    x,
                    y - hauteur + 20,
                    largeur,
                    hauteur
                )
            )

        elif nom_type_obstacle == "pique":
            x = obstacle.x
            y = 600 - obstacle.y

            pygame.draw.polygon(
                self.ecran,
                pygame.Color("orange"),
                [
                    (x, y),
                    (x + obstacle.taille, y),
                    (x + obstacle.taille / 2, y - obstacle.taille)
                ]
            )

    def dessiner(self):
        self.ecran.fill(pygame.Color("black"))
        pygame.draw.rect(
            self.ecran,
            pygame.Color("white"),
            pygame.Rect(
                self.jeu.joueur.x,
                600 - self.jeu.joueur.y - 50,
                50,
                50
            )
        )

        for obstacle in self.jeu.obstacles:
            self.dessiner_obstacle(obstacle)

jeu = Jeu()


# ============================================================
# FONCTIONS POUR CONSTRUIRE LE NIVEAU
# ============================================================

def ajouter_pique(x, y=0, taille=50):
    jeu.ajouter_obstacle(
        pique(x, y, taille)
    )


def ajouter_carre(x, y=0, taille=50):
    jeu.ajouter_obstacle(
        carre(x, y, taille)
    )


def ajouter_plateforme(x, y):
    jeu.ajouter_obstacle(
        plateforme(x, y)
    )


def ajouter_plateforme_forcee(x, y):
    """
    Plateforme de largeur 150 avec des piques en dessous.

    La plateforme est ajoutée AVANT les piques afin que
    get_state() voie d'abord la plateforme lorsque les deux
    commencent au même x.
    """

    ajouter_plateforme(x, y)

    taille_pique = min(50, y)

    ajouter_pique(
        x,
        0,
        taille_pique
    )

    ajouter_pique(
        x + 50,
        0,
        taille_pique
    )

    ajouter_pique(
        x + 100,
        0,
        taille_pique
    )


# ============================================================
# NIVEAU
# ============================================================


# ============================================================
# ZONE 1 : DÉBUT FACILE
# ============================================================

ajouter_pique(700)

ajouter_pique(1100)

ajouter_carre(1500)

ajouter_pique(1950)

ajouter_carre(2350)

ajouter_pique(2800)


# ============================================================
# ZONE 2 : PREMIERS ENCHAÎNEMENTS
# ============================================================

ajouter_pique(3200)
ajouter_pique(3260)

ajouter_carre(3700)

ajouter_pique(4120)
ajouter_pique(4180)

ajouter_carre(
    4600,
    0,
    70
)

ajouter_pique(5000)


# ============================================================
# ZONE 3 : PREMIÈRES PLATEFORMES
# ============================================================

ajouter_plateforme_forcee(
    5400,
    60
)

ajouter_pique(5800)

ajouter_plateforme_forcee(
    6150,
    90
)

ajouter_pique(6550)
ajouter_pique(6610)

ajouter_carre(7050)


# ============================================================
# ZONE 4 : PIQUES + CARRÉS
# ============================================================

ajouter_pique(7450)

ajouter_carre(7750)

ajouter_pique(8150)
ajouter_pique(8210)

ajouter_carre(
    8600,
    0,
    60
)

ajouter_pique(9000)

ajouter_carre(9350)

ajouter_pique(9670)


# ============================================================
# ZONE 5 : PLATEFORMES SUCCESSIVES
# ============================================================

ajouter_plateforme_forcee(
    10100,
    50
)

ajouter_plateforme_forcee(
    10450,
    80
)

ajouter_plateforme_forcee(
    10800,
    110
)

ajouter_plateforme_forcee(
    11150,
    80
)

ajouter_plateforme_forcee(
    11500,
    50
)

ajouter_pique(11900)


# ============================================================
# ZONE 6 : RYTHME PLUS RAPIDE
# ============================================================

ajouter_pique(12250)
ajouter_pique(12310)

ajouter_carre(12650)

ajouter_pique(13000)

ajouter_carre(13300)

ajouter_pique(13600)
ajouter_pique(13660)

ajouter_carre(
    14000,
    0,
    70
)

ajouter_pique(14350)


# ============================================================
# ZONE 7 : CARRÉS COMME PLATEFORMES
# ============================================================

ajouter_carre(
    14700,
    0,
    80
)

ajouter_carre(
    15050,
    0,
    100
)

ajouter_carre(
    15400,
    0,
    70
)

ajouter_pique(15800)


# ============================================================
# ZONE 8 : PLATEFORMES + OBSTACLES
# ============================================================

ajouter_plateforme_forcee(
    16150,
    60
)

ajouter_pique(16500)
ajouter_pique(16560)

ajouter_plateforme_forcee(
    16850,
    90
)

ajouter_carre(17200)

ajouter_plateforme_forcee(
    17550,
    120
)

ajouter_pique(17950)

ajouter_plateforme_forcee(
    18300,
    80
)


# ============================================================
# ZONE 9 : SECTION DENSE
# ============================================================

ajouter_pique(18700)
ajouter_pique(18760)

ajouter_carre(19050)

ajouter_pique(19350)

ajouter_carre(
    19600,
    0,
    60
)

ajouter_pique(19900)
ajouter_pique(19960)

ajouter_carre(
    20300,
    0,
    80
)

ajouter_pique(20650)

ajouter_pique(20950)
ajouter_pique(21010)


# ============================================================
# ZONE 10 : ESCALIER DE PLATEFORMES
# ============================================================

ajouter_plateforme_forcee(
    21400,
    40
)

ajouter_plateforme_forcee(
    21700,
    70
)

ajouter_plateforme_forcee(
    22000,
    100
)

ajouter_plateforme_forcee(
    22300,
    130
)

ajouter_plateforme_forcee(
    22600,
    100
)

ajouter_plateforme_forcee(
    22900,
    70
)

ajouter_plateforme_forcee(
    23200,
    40
)


# ============================================================
# ZONE 11 : RETOUR AU SOL
# ============================================================

ajouter_pique(23600)

ajouter_carre(23950)

ajouter_pique(24300)
ajouter_pique(24360)

ajouter_carre(24700)

ajouter_pique(25050)

ajouter_carre(
    25350,
    0,
    70
)

ajouter_pique(25700)

ajouter_pique(26000)
ajouter_pique(26060)

ajouter_carre(
    26400,
    0,
    60
)

ajouter_pique(26800)


# ============================================================
# ZONE 12 : HAUTEURS
# ============================================================

ajouter_plateforme_forcee(
    27200,
    70
)

ajouter_plateforme_forcee(
    27550,
    120
)

ajouter_plateforme_forcee(
    27900,
    150
)

ajouter_plateforme_forcee(
    28250,
    110
)

ajouter_plateforme_forcee(
    28600,
    70
)

ajouter_pique(29000)


# ============================================================
# ZONE 13 : DIFFICILE
# ============================================================

ajouter_pique(29300)
ajouter_pique(29360)

ajouter_carre(
    29700,
    0,
    70
)

ajouter_pique(30050)

ajouter_carre(30350)

ajouter_pique(30650)
ajouter_pique(30710)

ajouter_plateforme_forcee(
    31050,
    70
)

ajouter_pique(31400)

ajouter_plateforme_forcee(
    31700,
    110
)

ajouter_carre(
    32050,
    0,
    70
)

ajouter_pique(32400)
ajouter_pique(32460)


# ============================================================
# ZONE 14 : ALTERNANCE
# ============================================================

ajouter_carre(32800)

ajouter_pique(33100)

ajouter_carre(33400)

ajouter_pique(33700)

ajouter_plateforme_forcee(
    34000,
    70
)

ajouter_pique(34350)

ajouter_carre(
    34650,
    0,
    60
)

ajouter_pique(35000)
ajouter_pique(35060)

ajouter_plateforme_forcee(
    35400,
    100
)


# ============================================================
# ZONE 15 : FINAL
# ============================================================

ajouter_pique(35800)

ajouter_pique(36100)
ajouter_pique(36160)

ajouter_carre(
    36500,
    0,
    70
)

ajouter_plateforme_forcee(
    36850,
    70
)

ajouter_plateforme_forcee(
    37200,
    110
)

ajouter_pique(37600)

ajouter_carre(
    37950,
    0,
    80
)

ajouter_pique(38300)
ajouter_pique(38360)

ajouter_plateforme_forcee(
    38700,
    100
)

ajouter_carre(
    39100,
    0,
    60
)

ajouter_pique(39500)

ajouter_pique(39800)
ajouter_pique(39860)

ajouter_carre(
    40300,
    0,
    50
)

print(jeu.obstacles)
jeu.reset()
