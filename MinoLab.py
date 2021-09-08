import time
import sys
import random
            
            # gérer agents quand très proches ; tango à eviter
            
            
            
            
            

class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.caractere = '#'
        self.type = 1
        self.humains = []
        self.minotaures = []
        self.odeur_humain = 0
        self.nouvelle_odeur_humain = 0

    def est_un_mur(self):
        return self.caractere == '#'

    def transformer_chemin(self):
        self.caractere = ' '
        self.type = 0

    def transformer_mur(self):
        self.caractere = '#'
        self.type = 1

    def transformer_sortie(self):
        self.caractere = '@'
        self.type = 2

    def deposer_odeur(self, quantite):
        self.odeur_humain += quantite
        if self.odeur_humain > 1:
            self.odeur_humain = 1
    def reinitialiser_caractere(self):
        if self.type == 0:
            self.caractere = ' '
        elif self.type == 1:
            self.caractere = '#'
        elif self.type == 2:
            self.caractere = '@'






class Labyrinthe:
    def __init__(self, largeur, hauteur):
        self.largeur = int(largeur)
        self.hauteur = int(hauteur)
        self.labyrinthe = []

        self.total_odeur_humain = 0
        self.facteur_propagation_odeur = 0.5
        self.facteur_evaporation_odeur = 0.05

        self.initialiser()
        self.generer()

    def set_fact_propa(self, facteur_propagation):
        self.facteur_propagation_odeur = facteur_propagation
        if self.facteur_propagation_odeur > 1:
            self.facteur_propagation_odeur = 1
        elif self.facteur_propagation_odeur < 0:
            self.facteur_propagation_odeur = 0

    def set_fact_evap(self, facteur_evaporation):
        self.facteur_evaporation_odeur = facteur_evaporation
        if self.facteur_evaporation_odeur > 1:
            self.facteur_evaporation_odeur = 1
        elif self.facteur_evaporation_odeur < 0:
            self.facteur_evaporation_odeur = 0

    def initialiser(self):
        ligne = []
        for i in range(0, self.hauteur):
            for j in range(0, self.largeur):
                ligne.append(Case(j, i))
            self.labyrinthe.append(ligne)
            ligne = []

    def generer(self):
        self.get_case(1, 1).transformer_chemin()
        murs_restants = [self.get_case(1, 2), self.get_case(2, 1)]

        while len(murs_restants) > 0:
            # os.system("cls")
            # self.afficher()   # POUR VOIR LA GENERATION DU LABYRINTHE
            # print("\n\n")     # POUR VOIR LA GENERATION DU LABYRINTHE
            mur_actuel = random.choice(murs_restants)

            x = mur_actuel.x
            y = mur_actuel.y

            # Remove the wall if the condition is true
            if (self.a_3_murs_autour(x, y)
                    and self.verification_diagonale(x, y)):
                # self.set_maze_tile(x, y, " ")
                mur_actuel.transformer_chemin()

                # Add the walls around to the murs_restants
                # Top
                if self.a_3_murs_autour(x, y - 1):
                    murs_restants.append(self.get_case(x, y - 1))
                # Bottom
                if self.a_3_murs_autour(x, y + 1):
                    murs_restants.append(self.get_case(x, y + 1))
                # Left
                if self.a_3_murs_autour(x - 1, y):
                    murs_restants.append(self.get_case(x - 1, y))
                # Right
                if self.a_3_murs_autour(x + 1, y):
                    murs_restants.append(self.get_case(x + 1, y))

            murs_restants.remove(mur_actuel)
        self.ajouter_sortie()

    def get_case(self, x, y):
        return self.labyrinthe[y][x]

    def getEnv(self, x, y):
        case = self.get_case(x, y)
        return [case.type, case.minotaures, case.humains, case.odeur_humain]

    def est_un_mur(self, x, y):
        if self.est_dans_labyrinthe(x, y):
            if self.get_case(x, y).est_un_mur():
                return 1
            else:
                return 0
        else:
            return 1

    def a_3_murs_autour(self, x, y):
        if self.est_dans_labyrinthe(x, y) and self.est_un_mur(x, y):
            # Check the top tile
            number_of_walls_around = self.est_un_mur(x, y - 1)
            # Check the bottom tile
            number_of_walls_around += self.est_un_mur(x, y + 1)
            # Check the left tile
            number_of_walls_around += self.est_un_mur(x - 1, y)
            # Check the right tile
            number_of_walls_around += self.est_un_mur(x + 1, y)

            return number_of_walls_around == 3
        else:
            return 0

    def verification_diagonale(self, x, y):
        return (self.verification_4_diagonales(x, y, x - 1, y - 1)
                and self.verification_4_diagonales(x, y, x + 1, y - 1)
                and self.verification_4_diagonales(x, y, x + 1, y + 1)
                and self.verification_4_diagonales(x, y, x - 1, y + 1))

    def verification_4_diagonales(self, from_x, from_y, to_x, to_y):
        if not self.est_dans_labyrinthe(to_x, to_y):
            return True
        if not self.est_un_mur(to_x, to_y):
            if self.est_un_mur(from_x, to_y) and self.est_un_mur(to_x, from_y):
                return False
        return True

    def est_dans_labyrinthe(self, x, y):
        return 0 < x < (self.largeur - 1) and 0 < y < (self.hauteur - 1)

    def ajouter_sortie(self):
        while True:
            x = random.randrange(1, self.largeur)
            y = random.randrange(1, self.hauteur)
            if not self.est_un_mur(x, y):
                self.get_case(x, y).transformer_sortie()
                break

    def calculer_total_odeur_humain(self):
        self.total_odeur_humain = 0
        for x in range(self.largeur):
            for y in range(self.hauteur):
                self.total_odeur_humain += self.get_case(x, y).odeur_humain

    def deposer_odeur(self, x, y, quantite):
        self.get_case(x, y).deposer_odeur(quantite)
        self.calculer_total_odeur_humain()

    def get_odeur(self, x, y):
        return self.get_case(x, y).odeur_humain

    def propager_odeurs(self):
        # Matrice des
        for x in range(self.largeur):
            for y in range(self.hauteur):
                case = self.get_case(x, y)
                case.nouvelle_odeur_humain = case.odeur_humain

        # Propagation des odeurs
        for x in range(self.largeur):
            for y in range(self.hauteur):
                # Si la case a une odeur
                case = self.get_case(x, y)
                if case.odeur_humain != 0:
                    self.propager_odeur_case(case)

        # Evaporation des odeurs
        for x in range(self.largeur):
            for y in range(self.hauteur):
                case = self.get_case(x, y)
                case.nouvelle_odeur_humain -= case.nouvelle_odeur_humain * self.facteur_evaporation_odeur

        # Remplacer les anciennes valeurs par les nouvelles calculées
        for x in range(self.largeur):
            for y in range(self.hauteur):
                case = self.get_case(x, y)
                case.odeur_humain = case.nouvelle_odeur_humain
                if case.odeur_humain < 0.001:
                    case.odeur_humain = 0

        self.calculer_total_odeur_humain()

    def propager_odeur_case(self, case):
        nombre_cases_propagees = 0
        x = case.x
        y = case.y
        # Au dessus
        nombre_cases_propagees += self.propager_odeur_de_vers(case, x, y-1)
        # En dessous
        nombre_cases_propagees += self.propager_odeur_de_vers(case, x, y+1)
        # À gauche
        nombre_cases_propagees += self.propager_odeur_de_vers(case, x-1, y)
        # À droite
        nombre_cases_propagees += self.propager_odeur_de_vers(case, x+1, y)

        # Retirer la quantité d'odeur propagée de la case actuelle
        case.nouvelle_odeur_humain -= ((case.odeur_humain * self.facteur_propagation_odeur) / 4) * nombre_cases_propagees

    # Retourne 0 si l'odeur n'a pas été propagée, 1 si elle a été propagée
    def propager_odeur_de_vers(self, case, to_x, to_y):
        if not self.est_un_mur(to_x, to_y):
            case_voisine = self.get_case(to_x, to_y)
            case_voisine.nouvelle_odeur_humain += (case.odeur_humain * self.facteur_propagation_odeur) / 4
            return 1
        return 0

    def afficher(self):
        res = ""
        for i in range(self.hauteur):
            for j in range(self.largeur):
                res += self.labyrinthe[i][j].caractere + ' '
            res += "\n"
        print(res)

    def afficher_odeurs_nombres(self):
        print(f"Total odeur humain = {self.total_odeur_humain}")
        res = ""
        for y in range(self.hauteur):
            for x in range(self.largeur):
                res += "{:.3f}".format(self.get_odeur(x, y)) + '\t\t'
            res += "\n"
        print(res)

    def afficher_odeurs_visu(self):
        res = ""
        for y in range(self.hauteur):
            for x in range(self.largeur):
                odeur = self.get_odeur(x, y)
                if odeur > 0.500:
                    res += "▓ "
                elif odeur > 0.100:
                    res += "▒ "
                elif odeur > 0.020:
                    res += "░ "
                else:
                    res += self.labyrinthe[y][x].caractere + " "
            res += "\n"
        print(res)




class Minotaure:
    def __init__ (self, posX, posY,labyrinthe):
        self.posX=posX
        self.posY=posY
        self.face = 'N'
        self.tmpsEtourdi=0
        self.vitesse = 1
        self.enRuee=False
        labyrinthe.getEnv(posX,posY)[1].append(self)
        
        
    def humAPorte(self,labyrinthe):
        if (len(labyrinthe.getEnv(self.posX,self.posY)[2])>0) :
            return True
        if self.face=='S' and len(labyrinthe.getEnv(self.posX,self.posY+1)[2]) > 0 :
            return(True)
        elif self.face=='N' and len(labyrinthe.getEnv(self.posX,self.posY-1)[2]) > 0 :
            return(True)
        elif self.face=='E' and len(labyrinthe.getEnv(self.posX+1,self.posY)[2]) > 0 :
            return(True)
        elif self.face=='W' and len(labyrinthe.getEnv(self.posX,self.posY-1)[2]) > 0 :
            return(True)
        return(False)
       
        
    def toString(self) :
        return ("ma pos : " + str(self.posX) + ' , ' + str(self.posY) + ", je regarde : " + self.face + " . suis-je etourdi ? " + str(self.tmpsEtourdi) + '. suis je en ruee ? ' + str(self.enRuee))
    
        
    def go(self,labyrinthe):
        for i in range(self.vitesse):
            if self.enRuee:
                self.ruee(labyrinthe)
                self.avancer()
            else :
                self.chercher(labyrinthe)
                if self.tmpsEtourdi>0 :
                    self.tmpsEtourdi -=1
                elif self.humainDansChampDeVision(labyrinthe) :
                    self.ruee(labyrinthe)
                    self.avancer(labyrinthe)
                elif labyrinthe.getEnv(self.posX,self.posY)[3]>0:
                    self.suivreOdeur(labyrinthe,labyrinthe.getEnv(self.posX,self.posY)[3])
                    self.avancer(labyrinthe)
                else :
                    self.avancer(labyrinthe)
            if self.humainDansChampDeVision(labyrinthe) and self.humAPorte(labyrinthe) and self.tmpsEtourdi==0:
                self.tuer(labyrinthe)
            #maze.afficher()
            
    def chercher(self,labyrinthe) :
        listeRes=[]
        for i in [0,1,2] :
            if self.peutAvancer(i,labyrinthe)[0] :  
                listeRes.append(i)
        if len(listeRes) == 0 :
            if self.face=="N":
                self.face='S'
            elif self.face=="E":
                self.face='W'
            elif self.face=="S":
                self.face="N"
            elif self.face=="W":
                self.face='E'
        else :   
            i=listeRes[random.randint(0,len(listeRes)-1)]
            if self.face=='N':
                if i==1:
                    self.face='E'
                if i==0:
                    self.face='N'
                if i==2:
                    self.face='W'
            elif self.face=='E' :
                if i==1:
                    self.face='S'
                if i==0:
                    self.face='E'
                if i==2:
                    self.face='N'
            elif self.face=='S' :
                if i==1:
                    self.face='W'
                if i==0:
                    self.face='S'
                if i==2:
                    self.face='E'
            elif self.face=='W':
                if i==1:
                    self.face='N'
                if i==0:
                    self.face='W'
                if i==2:
                    self.face='S'
            

        
        
        
        
        
    def murProche(self,labyrinthe):
        nbMur=0
        for i in [-1,1]:
            if labyrinthe.getEnv(self.posX+i,self.posY)[0] == 1 :
                nbMur+=1
            if labyrinthe.getEnv(self.posX, self.posY+i)[0] == 1 :
                nbMur+=1
        return(nbMur)
    
    def peutAvancer(self,direction,labyrinthe) :   # getEnv(x,y) renvoie [couloir.mur,minotaure,humain,odeur]
        if direction == 0 :
            if self.face=='S' and labyrinthe.getEnv(self.posX,self.posY+1)[0] !=1 :
                return(True,self.posX, self.posY+1)
            elif self.face=='N' and labyrinthe.getEnv(self.posX,self.posY-1)[0] !=1 :
                return(True,self.posX, self.posY-1)
            elif self.face=='E' and labyrinthe.getEnv(self.posX+1,self.posY)[0] !=1 :
                return(True,self.posX+1, self.posY)
            elif self.face=='W' and labyrinthe.getEnv(self.posX-1,self.posY)[0] !=1 :
                return(True,self.posX-1, self.posY)
                
        if direction == 1 :
            if self.face=='S' and labyrinthe.getEnv(self.posX-1,self.posY)[0] !=1 :
                return(True,self.posX-1, self.posY)
            elif self.face=='N' and labyrinthe.getEnv(self.posX+1,self.posY)[0] !=1 :
                return(True,self.posX+1, self.posY)
            elif self.face=='E' and labyrinthe.getEnv(self.posX,self.posY+1)[0] !=1 :
                return(True,self.posX, self.posY+1)
            elif self.face=='W' and labyrinthe.getEnv(self.posX,self.posY-1)[0] !=1 :
                return(True,self.posX, self.posY-1)
                
        if direction == 2 :
            if self.face=='S' and labyrinthe.getEnv(self.posX+1,self.posY)[0] !=1 :
                return(True,self.posX+1, self.posY)
            elif self.face=='N' and labyrinthe.getEnv(self.posX-1,self.posY)[0] !=1 :
                return(True,self.posX-1, self.posY)
            elif self.face=='E' and labyrinthe.getEnv(self.posX,self.posY-1)[0] !=1 :
                return(True,self.posX, self.posY-1)
            elif self.face=='W' and labyrinthe.getEnv(self.posX,self.posY+1)[0] !=1 :
                return(True,self.posX, self.posY+1)
                
        if direction == 3 :
            if self.face=='S' and labyrinthe.getEnv(self.posX,self.posY-1)[0] !=1 :
                return(True,self.posX, self.posY-1)
            elif self.face=='N' and labyrinthe.getEnv(self.posX,self.posY+1)[0] !=1 :
                return(True,self.posX, self.posY+1)
            elif self.face=='E' and labyrinthe.getEnv(self.posX-1,self.posY)[0] !=1 :
                return(True,self.posX-1, self.posY)
            elif self.face=='W' and labyrinthe.getEnv(self.posX+1,self.posY)[0] !=1 :
                return(True,self.posX+1, self.posY)
        return(False,0,0)
                
    def avancer(self,labyrinthe):
        labyrinthe.getEnv(self.posX,self.posY)[1].remove(self)
        if self.face=="N" :
            self.posY-=1
        elif self.face=="E":
            self.posX+=1
        elif self.face=="S" :
            self.posY+=1
        else :
            self.posX-=1
        labyrinthe.getEnv(self.posX,self.posY)[1].append(self)
    
    def findFace(self,labyrinthe,dir):
        if self.face=='N':
            if dir==0:
                return('N')
            if dir==1:
                return('E')
            if dir==2:
                return('W')
            if dir==3:
                return('S')
        if self.face=='E':
            if dir==0:
                return('E')
            if dir==1:
                return('S')
            if dir==2:
                return('N')
            if dir==3:
                return('W')
        if self.face=='S':
            if dir==0:
                return('S')
            if dir==1:
                return('W')
            if dir==2:
                return('E')
            if dir==3:
                return('N')
        if self.face=='W':
            if dir==0:
                return('W')
            if dir==1:
                return('N')
            if dir==2:
                return('S')
            if dir==3:
                return('E')
    
    def suivreOdeur(self,labyrinthe,degOdeur):
        maxOdeur = degOdeur
        #if(self.murProche() == 3):
        maxDir = 0
        for dir in range(4):
            resPeutAvancer=self.peutAvancer(dir,labyrinthe)
            if(resPeutAvancer[0] and labyrinthe.getEnv(resPeutAvancer[1],resPeutAvancer[2])[3] > maxOdeur):
                maxOdeur = labyrinthe.getEnv(resPeutAvancer[1],resPeutAvancer[2])[3]
                maxDir = dir
        self.face=self.findFace(labyrinthe,maxDir)
        
        
    def humainDansChampDeVision(self,labyrinthe):
        
        if self.face=='N':
            varpos=self.posY-1
            while len(labyrinthe.getEnv(self.posX,varpos)[2])==0 and labyrinthe.getEnv(self.posX,varpos)[0]!=1:
                varpos+=1
            return(len(labyrinthe.getEnv(self.posX,varpos)[2])>0)
        elif self.face=='S':
            varpos=self.posY+1
            while len(labyrinthe.getEnv(self.posX,varpos)[2])==0 and labyrinthe.getEnv(self.posX,varpos)[0]!=1:
                varpos-=1
            return(len(labyrinthe.getEnv(self.posY,varpos)[2])>0)
        elif self.face=='E':
            varpos=self.posX+1
            while len(labyrinthe.getEnv(varpos,self.posY)[2])==0 and labyrinthe.getEnv(varpos,self.posY)[0]!=1:
                varpos+=1
            return(len(labyrinthe.getEnv(varpos,self.posY)[2])>0)
        else: 
            varpos=self.posX-1
            while len(labyrinthe.getEnv(varpos,self.posY)[2])==0 and labyrinthe.getEnv(varpos,self.posY)[0]!=1:
                varpos-=1
            return(len(labyrinthe.getEnv(varpos,self.posY)[2])>0)
            
    def tuer(self,labyrinthe) :        # env(x,y) : [couloir/mur/sortie , [minotaures sur cette case] , [humains sur cette case] , odeur ]
    
    
        if self.face=='N':
            for hum in labyrinthe.getEnv(self.posX, self.posY-1)[2] :
                hum.vivant = False
        elif self.face=='S' :
            for hum in labyrinthe.getEnv(self.posX, self.posY+1)[2] :
                hum.vivant = False
        elif self.face=='E' :
            for hum in labyrinthe.getEnv(self.posX+1, self.posY)[2] :
                hum.vivant = False
        elif self.face=='W' :
            for hum in labyrinthe.getEnv(self.posX-1, self.posY)[2] :
                hum.vivant = False
    
            
            
    def ruee(self,labyrinthe):
        if self.peutAvancer(0,labyrinthe)[0] :
            self.vitesse=2
        else :
            self.enRuee=False
            self.tmpsEtourdi=10
            self.vitesse=1
            
            
class Humain:
    def __init__ (self, posX, posY,labyrinthe):
        self.posX=posX
        self.posY=posY
        self.face = 'N'
        self.vitesse = 1
        self.vivant = True
        self.onSortie = False
        labyrinthe.getEnv(posX,posY)[2].append(self)
        
    def go(self,labyrinthe):
        #if labyrinthe.getEnv(self.posX,self.posY)[0] == 2 :
            #self.sortir()
        for i in range(self.vitesse):
            if (self.vivant):
                self.chercher(labyrinthe)
                if self.minotaureDansChampsDeVision(labyrinthe) :
                    self.fuir(labyrinthe)
                self.avancer(labyrinthe)
                if labyrinthe.getEnv(self.posX,self.posY)[0] == 2 :
                    self.sortir()
            #maze.afficher()
            
    def findFace(self,labyrinthe,dir):
        if self.face=='N':
            if dir==0:
                return('N')
            if dir==1:
                return('E')
            if dir==2:
                return('W')
            if dir==3:
                return('S')
        if self.face=='E':
            if dir==0:
                return('E')
            if dir==1:
                return('S')
            if dir==2:
                return('N')
            if dir==3:
                return('W')
        if self.face=='S':
            if dir==0:
                return('S')
            if dir==1:
                return('W')
            if dir==2:
                return('E')
            if dir==3:
                return('N')
        if self.face=='W':
            if dir==0:
                return('W')
            if dir==1:
                return('N')
            if dir==2:
                return('S')
            if dir==3:
                return('E')
            
            
    def toString(self) :
        return ("ma pos : " + str(self.posX) + ' , ' + str(self.posY) + ", je regarde : " + self.face + ". suis je vivant ? " + str(self.vivant))
            
    
    def minotaureDansChampsDeVision(self,labyrinthe):
        
        if self.face=='N':
            varpos=self.posY-1
            print(len(labyrinthe.getEnv(self.posX,varpos)[1])==0)
            while len(labyrinthe.getEnv(self.posX,varpos)[1])==0 and labyrinthe.getEnv(self.posX,varpos)[0]!=1:
                
                #maze.afficher()
                varpos-=1
            return(len(labyrinthe.getEnv(self.posX,varpos)[1])>0)
        elif self.face=='S':
            varpos=self.posY+1
            print(len(labyrinthe.getEnv(self.posX,varpos)[1])==0)
            while len(labyrinthe.getEnv(self.posX,varpos)[1])==0 and labyrinthe.getEnv(self.posX,varpos)[0]!=1:
                
                #maze.afficher()
                varpos+=1
            return(len(labyrinthe.getEnv(self.posX,varpos)[1])>0)
        elif self.face=='E':
            varpos=self.posX+1
            print(len(labyrinthe.getEnv(varpos,self.posY)[1])==0)
            while (len(labyrinthe.getEnv(varpos,self.posY)[1])==0 and labyrinthe.getEnv(varpos,self.posY)[0]!=1):
                
                #maze.afficher()
                varpos+=1
            return(len(labyrinthe.getEnv(varpos,self.posY)[1])>0)
        else: 
            varpos=self.posX-1
            print(len(labyrinthe.getEnv(varpos,self.posY)[1])==0)
            while len(labyrinthe.getEnv(varpos,self.posY)[1])==0 and labyrinthe.getEnv(varpos,self.posY)[0]!=1:
                
                #maze.afficher()
                varpos-=1
            return(len(labyrinthe.getEnv(varpos,self.posY)[1])>0)
    
    
    def avancer(self,labyrinthe):
        labyrinthe.getEnv(self.posX,self.posY)[2].remove(self)
        if self.face=="N" :
            self.posY-=1
        elif self.face=="E":
            self.posX+=1
        elif self.face=="S" :
            self.posY+=1
        else :
            self.posX-=1
        labyrinthe.getEnv(self.posX,self.posY)[2].append(self)
        
        
    def peutAvancer(self,direction,labyrinthe) :
        
        if direction == 0 :                                                                             # devant
            if self.face=='S' and labyrinthe.getEnv(self.posX,self.posY+1)[0] != 1 :
                return(True,self.posX, self.posY+1)
            elif self.face=='N' and labyrinthe.getEnv(self.posX,self.posY-1)[0] != 1 :
                return(True,self.posX, self.posY-1)
            elif self.face=='E' and labyrinthe.getEnv(self.posX+1,self.posY)[0] != 1 :
                return(True,self.posX+1, self.posY)
            elif self.face=='W' and labyrinthe.getEnv(self.posX-1,self.posY)[0] != 1 :
                return(True,self.posX-1, self.posY)
            return(False,0,0)
        if direction == 1 :                                                                             # droite
            if self.face=='S' and labyrinthe.getEnv(self.posX-1,self.posY)[0] != 1 :
                return(True,self.posX-1, self.posY)
            elif self.face=='N' and labyrinthe.getEnv(self.posX+1,self.posY)[0] !=1 :
                return(True,self.posX+1, self.posY)
            elif self.face=='E' and labyrinthe.getEnv(self.posX,self.posY+1)[0] !=1 :
                return(True,self.posX, self.posY+1)
            elif self.face=='W' and labyrinthe.getEnv(self.posX,self.posY-1)[0] !=1 :
                return(True,self.posX, self.posY-1)
            return(False,0,0)
                
        if direction == 2 :                                                                             # gauche
            if self.face=='S' and labyrinthe.getEnv(self.posX+1,self.posY)[0] !=1 :
                return(True,self.posX+1, self.posY)
            elif self.face=='N' and labyrinthe.getEnv(self.posX-1,self.posY)[0] !=1 :
                return(True,self.posX-1, self.posY)
            elif self.face=='E' and labyrinthe.getEnv(self.posX,self.posY-1)[0] !=1 :
                return(True,self.posX, self.posY-1)
            elif self.face=='W' and labyrinthe.getEnv(self.posX,self.posY+1)[0] !=1 :
                return(True,self.posX, self.posY+1)
            return(False,0,0)
                
        if direction == 3 :                                                                             # derriere
            if self.face=='S' and labyrinthe.getEnv(self.posX,self.posY-1)[0] !=1 :
                return(True,self.posX, self.posY-1)
            elif self.face=='N' and labyrinthe.getEnv(self.posX,self.posY+1)[0] !=1 :
                return(True,self.posX, self.posY+1)
            elif self.face=='E' and labyrinthe.getEnv(self.posX-1,self.posY)[0] !=1 :
                return(True,self.posX-1, self.posY)
            elif self.face=='W' and labyrinthe.getEnv(self.posX+1,self.posY)[0] !=1 :
                return(True,self.posX+1, self.posY)
            return(False,0,0)
    
    
        
    def chercher(self,labyrinthe) :
        paspossible=0
        lastFace=self.face
        for i in [2,0,1] :
            listeRes=self.peutAvancer(i,labyrinthe)
            if listeRes[0] :  
                lastFace=self.findFace(labyrinthe,i)
            else :
                paspossible+=1
        self.face=lastFace
        if paspossible==3 :
            if self.face=="N":
                self.face='S'
            elif self.face=="E":
                self.face='W'
            elif self.face=="S":
                self.face="N"
            elif self.face=="W":
                self.face='E'
        
            

                    
            
    def fuir(self,labyrinthe):
        for i in [3,2,1] :
            listeRes=self.peutAvancer(i,labyrinthe)
            if listeRes[0] :  
                self.face=self.findFace(labyrinthe,i)
        
                
                
                
                

#            print("soucis"+"\n\n"+"soucis")
 #       elif self.face == 'W'and self.peutAvancer(3,labyrinthe) :
  #          #self.face = 'E'
   #         print("soucis"+"\n\n"+"soucis")
        # elif self.face == 'S'and self.peutAvancer(3,labyrinthe) :
        #     #self.face = 'N'
        #     print("soucis"+"\n\n"+"soucis")
        # elif self.peutAvancer(3,labyrinthe) :
        #     #self.face = 'W'
        #     print("soucis"+"\n\n"+"soucis")
        # 
            
    
    def sortir(self) :
        self.onSortie=True
        return()
            
            

            

            
            # fringe case : hum peut mourir entre arrivée sur sortie et next tick




# if __name__ == '__main__':
#     if len(sys.argv) != 3:
#         print("Pour lancer le programme : python3 main.py <hauteur> <longuer>")   
        
maxLen=15
maxHaut=10        
maze = Labyrinthe(maxLen,maxHaut)
# maze.afficher()

# maze=Labyrinthe(maxLen,3)

x=random.randrange(0,maxLen)
y=random.randrange(0,maxHaut)
xh=random.randrange(0,maxLen)
yh=random.randrange(0,maxHaut)
while (maze.est_un_mur(x,y)):
    x=random.randrange(0,maxLen)
    y=random.randrange(0,maxHaut)
    print("jétais un mur")
while (maze.est_un_mur(xh,yh)):
    xh=random.randrange(0,maxLen)
    yh=random.randrange(0,maxHaut)
    print("jétais un mur")
mino=Minotaure(x,y,maze)
hum=Humain(xh,yh,maze)
maze.get_case(x,y).caractere='0'
maze.get_case(xh,yh).caractere=hum.face
maze.afficher()
time.sleep(0.5)
print('\n\n\n\n')
while(not(hum.onSortie) and hum.vivant):
    maze.get_case(hum.posX,hum.posY).reinitialiser_caractere()
    hum.go(maze)
    maze.deposer_odeur(hum.posX,hum.posY,1)
    maze.propager_odeurs()
    maze.get_case(hum.posX,hum.posY).caractere=hum.face    
    print("hum : " + hum.toString())
    print('\n mino : '+mino.toString())
    maze.afficher()
    time.sleep(0.5)
    print('\n\n\n\n')
    maze.get_case(mino.posX,mino.posY).reinitialiser_caractere()
    mino.go(maze)
    maze.get_case(mino.posX,mino.posY).caractere=str(int(maze.getEnv(mino.posX,mino.posY)[3]*10))
    print("hum : " + hum.toString())
    print('\n mino : '+mino.toString())
    maze.afficher()
    time.sleep(0.5)
    print('\n\n\n\n')
            
            
            
            
            
            
            
            
            
            
            
            
