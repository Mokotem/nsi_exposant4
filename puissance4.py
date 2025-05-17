class PileMaisNormal:
    def __init__(self):
        self.__data = list()
        
    def add(self, value):
        self.__data.append(value)
        
    @property
    def peek(self): return self.__data[-1]
    
    def pop(self):
        if self.is_empty: raise Exception(":( la pile est vide")
        element = self.peek
        self.__data.pop(-1)
        return element

    @property
    def height(self): return len(self.__data)
    
    @property
    def is_empty(self): return len(self.__data) == 0

class Partie:
    def __init__(self, dim, taille_p: int, p1, p2):
        # la taille du plateau est variable
        self.dimention = dim
        self.grille = [Pile(dim.y) for _ in range(dim.x)]
        
        self.taille_puissance = taille_p
        
        self.j1 = p1
        self.j2 = p2
        
        self.joueur = p1
        self.est_j1 = True
        
        # si la partie est fini
        self.__finito = False
        self.__ligneChiffres = " "
        y = 0
        while y < self.dimention.x:
            self.__ligneChiffres += str(y + 1) + " "
            y += 1
            
        self.__pileDesCoups = PileMaisNormal()
        
    @property
    def finito(self):
        return self.__finito
        
    def defaire(self):
        """
        annule le dernier coup joue.
        """
        self.finito = False
        self.grille[self.__pileDesCoups.pop()].retirer()
        
    def alignes(self, pos):
        pion = self.grille[pos.x][pos.y]
        streak = 0
        p = Vecteur(0, 0)
        
        def check() -> bool:
            nonlocal streak
            if self.grille[p.x][p.y] == pion:
                streak += 1
                if (streak >= self.taille_puissance):
                    return True
            else:
                streak = 0
            return False
        mx = max(0, pos.x - self.taille_puissance)
        Mx = min(self.dimention.x - 1, pos.x + self.taille_puissance)
        p = Vecteur(mx, pos.y)
        while p.x < Mx:
            if check(): return True
            p.x += 1
        streak = 0
        Mx = min(self.dimention.y - 1, pos.y + self.taille_puissance)
        p = Vecteur(pos.x, 0)
        while p.y < Mx:
            if check(): return True
            p.y += 1
            
        mx = min(pos.x, pos.y)
        Mx = self.dimention.x - 1
        p = Vecteur(pos.x - mx, pos.y - mx)
        while p.x < Mx and p.y < self.dimention.y:
            if check(): return True
            p.x += 1
            p.y += 1
        streak = 0
        mx = min(self.dimention.x - pos.x - 1, pos.y)
        Mx = self.dimention.y
        p = Vecteur(pos.x + mx, pos.y - mx)
        while p.y < Mx and p.x >= 0:
            if check(): return True
            p.x -= 1
            p.y += 1
            
        return False
        
        
    
    
    
    def jouer_coup(self, colonne: int) -> None:
        """
        Fais tomber un pions dans une colonne selon le
        joueur a qui est le tour.
        utilise les attributs:
        'self.plateau', 'self.joueur.pion'
        (entree: int colonne)
        """
        self.grille[colonne].empiler(self.est_j1 + 1)
        self.__pileDesCoups.add(colonne)
        
        if self.alignes(Vecteur(colonne, len(self.grille[colonne]) - 1)):
            self.__finito = True
        else:
            self.est_j1 = not self.est_j1
            self.joueur = self.j1 if self.est_j1 else self.j2
    
    def coups_legaux(self) -> list:
        """
        renvoie les colonnes qui sont jouable sur le
        plateau, c'est a dire les colonnes non vides.
        (sortie: list int, ou les entiers designent le
        numero de la colonne)
        """
        res = list()
        i = 0
        while i < self.dimention.x:
            if (not self.grille[i].est_plein()):
                res.append(i)
            i += 1
        return res
    
    def afficher(self) -> None:
        print(self.__ligneChiffres)
        y = self.dimention.y - 1
        while y >= 0:
            ligne = "|"
            x = 0
            while x < self.dimention.x:
                if (self.grille[x][y] == 2):
                    ligne += str(self.j1.pion) + "|"
                elif (self.grille[x][y] == 1):
                    ligne += str(self.j2.pion) + "|"
                else:
                    ligne += " |"
                x += 1
            print(ligne)
            y += -1
        
        
class Pile:
    def __init__(self, longueur: int):
        self.__data = [0] * longueur  # initialise une pile vide de taille `longueur`

    def empiler(self, joueur: int):
        """
        ajoute une element (1 ou 2) a la pile.
        lance une erreur si elle est pleine.
        """
        for i in range(len(self.__data)):
            if self.__data[i] == 0:
                self.__data[i] = joueur
                return
        raise ValueError("Pile est pleine !")
    
    def retirer(self):
        if self.est_vide(): raise Exception("pile vide sah")
        i = len(self.__data) - 1
        while (self.__data[i] == 0):
            i += 1
        self.__data[i] = 0
    
    def est_vide(self) -> bool:
        return all(val == 0 for val in self.__data)

    def vider(self) -> None:
        self.__data = [0] * len(self.__data)

    def est_plein(self) -> bool:
        return all(val != 0 for val in self.__data)

    def __getitem__(self, index) -> int:
        return self.__data[index]

    def __len__(self) -> int:
        n = 0
        while n < len(self.__data) and self.__data[n] > 0:
            n += 1
        return n

    def __str__(self) -> str:
        return str(self.__data)
    
class Vecteur:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        pass
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
import time

class Joueur:
    def __init__(self, nom: str, char: int, t: int):
        """
        initialise un joueur avec un nom, un pion et un temps total pour jouer.
        :param nom: Nom du joueur
        :param char: Valeur numerique representant le pion (1 ou 2)
        :param t: Temps total en secondes pour jouer
        """
        self.nom = nom
        self.pion = char
        self.temps = t #temps en secondes

    def reste_du_temps(self) -> bool:
        """
        verifie s'il reste du temps au joueur.
        :return: True si le joueur a encore du temps, False sinon.
        """
        return self.temps > 0

    def choisir(self, choix: list) -> int:
        """
        propose une liste de choix au Joueur, et renvoie
        le choix qu'il a fait.
        /!\ recommence tant que son choix n'est pas valide
        /!\ retire au timer le temps mis pour choisir un coup
        """
        debut = time.time()
        coup = -1
        while coup not in choix:
            entree = input(self.nom + " (" + self.pion + ") " + str(round(self.temps)) + "s > ")
            i = 0
            while i < len(entree) and '0' <= entree[i] <= '9':#pour s'assurer que l'entree ne contient que des chiffres
                i += 1
            if i == len(entree) and len(entree) > 0:
                coup = int(entree) - 1
                if coup not in choix:
                    print("Cette colonne n'est pas jouable, essayez encore.")
            else:
                print("Entree invalide, veuillez entrer un nombre.")
        self.temps -= (time.time() - debut) #mise a jour de temps restant

        return coup

    def __str__(self) -> str:
        """
        retourne une representation sous forme de chaine du joueur.

        :return: Nom du joueur et pion associe.
        """
        return f"Joueur {self.nom} (Pion: {self.pion}, Temps restant: {int(self.temps)}s)"