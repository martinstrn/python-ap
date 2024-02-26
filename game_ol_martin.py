import pygame
import argparse
import logging

#CONSTANTES
ITER=3


def coord_pts_autour(coord):
    #prend en entrée un tuple de coordonnées et renvoie la liste des coordonnées des points autours
    x,y=coord
    return [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]

#Lire les arguments
def read_args():
    parser = argparse.ArgumentParser(description="Game of Life Simulation")
    # Ajouter les arguments de ligne de commande 
    parser.add_argument("-i", "--input", help="Path to the initial pattern file.")
    parser.add_argument("-o", "--output",default='current_state___.txt',help="Path to the output file.")
    parser.add_argument("-m", "--steps", type=int, default=20, help="Number of steps to run.")
    parser.add_argument("-d", "--display", action="store_true", help="Display the simulation step by step.")
    parser.add_argument("-f", "--fps", type=int, default=10, help="Number of frames per second.")
    parser.add_argument("--width", type=int, default=800, help="Initial width of the pygame screen.")
    parser.add_argument("--height", type=int, default=600, help="Initial height of the pygame screen.")
    return parser.parse_args()

class Cell:
    def __init__(self,coord, dic,etat=1):
        #dic est le dictionnaire des points vivants
        self.state = etat
        self._coord=coord
        self._nbrvoisin = 0
        self._dic={key:dic[key].state for key in dic.keys() }
        self.new_state=etat

    def nbr_voisin(self):
        #prend en entrée le dictionnaire des cellules vivantes, qui a pour clef
        liste_coord_voisin=coord_pts_autour(self._coord)
        for coord in liste_coord_voisin:
            if coord in self._dic :
                if self._dic[coord]==1:
                    self._nbrvoisin+=1
        
    def change_state(self):
        #on change l'état de la cellule en fonction de ses voisins
        self.nbr_voisin()
        if self.state==0:
            if self._nbrvoisin==3:
                self.new_state=1
        else :
            if self._nbrvoisin>3 or self._nbrvoisin<=1:
                self.new_state=0


def convert_into_list_of_list(pattern):
    #fonction qui prend en entrée un pattern sous forme de liste de str et qui renvoie une liste de liste
    return [list(pattern[i]) for i in range(len(pattern))]



class CellSet:
    def __init__(self, initial_pattern):
        #le pattern inital est une liste de str
        self.grid=convert_into_list_of_list(initial_pattern)
        self.dico={}
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j]=='1':
                    #on crée un objet cellule pour chaque cellule vivante, les clefs du dictionnaire sont les coordonnées
                    self.dico[(i,j)]=Cell((i,j),self.dico,1)
        self._out=None

    def add_dead_cells(self):
        #fonction pour ajouter les cellules mortes au cas où elles deviendraient vivantes à l'instant suivant
        #on crée un dictionnaire temporaire pour ne pas modifier le dictionnaire actuel
        dico1=self.dico.copy()
        #on parcours toutes les cellules vivantes à l'état actuel
        for coord in dico1:
            for coord_voisin in coord_pts_autour(coord):
                #on regarde si ses voisins sont morts
                if coord_voisin not in self.dico:
                    self.dico[coord_voisin]=Cell(coord_voisin,self.dico,0)

    def update_all_neighbours(self):
        #mettre à jour les cellules autour de chaque cellule
        for coord in self.dico:
            self.dico[coord]=Cell(coord,self.dico,self.dico[coord].state)
        

    def only_keep_living_cell(self):
        #on veut supprimer les cellules mortes
        dico1=self.dico.copy()
        for coord in dico1:
            #on teste le nouvel état uniquement
            if dico1[coord].new_state==0:
                del self.dico[coord]
            else:
                self.dico[coord].state=1

    def calculate_next_state(self):
        # Calculer l'état suivant pour chaque cellule
        self.add_dead_cells()
        #maintenant on a toutes les cellules vivantes et mortes autour des cellules vivantes à l'état actuel
        self.update_all_neighbours()
        for key_coord in self.dico:
            self.dico[key_coord].change_state()
        self.only_keep_living_cell()

    def get_dico(self):
        return self.dico
    

    def save_state(self, output_file):
        # Sauvegarder l'état des cellules dans un fichier
        # Le format du fichier est le suivant: un fichier texte avec des lignes de 0 et de 1
        min_x=min(self.dico.keys(),key=lambda x:x[0])[0]
        min_y=min(self.dico.keys(),key=lambda x:x[1])[1]
        max_x=max(self.dico.keys(),key=lambda x:x[0])[0]
        max_y=max(self.dico.keys(),key=lambda x:x[1])[1]
        self._out=[["0" for j in range(min_y,max_y+1)] for i in range(min_x,max_x+1)]
        for coord in self.dico:
            x,y=coord
            self._out[x-min_x][y-min_y]="1"
        with open(output_file,'w') as f:
            for line in self._out:
                f.write(''.join(line)+'\n')
        return


class Simulation_and_Display():
    def __init__(self):
        self._current_iter=0
        self.args = read_args()

        #création des attributs liés aux arguments
        self._max_iter=self.args.steps
        self._fps=self.args.fps

        #dimension de la fenêtre
        self._width=self.args.width
        self._height=self.args.height
        

        #le pattern initial est renseigné par un des arguments
        path=self.args.input
        with open(path,'r') as f:
            self._initial_pattern=[line.strip() for line in f]
        #self.tile_size=min(self._width//len(self._initial_pattern[0]),self._height//len(self._initial_pattern))
        self.tile_size=20
        #à voir si on veut respecter la demande de fenêtre de l'utilisateur
        self._width=len(self._initial_pattern[0])*self.tile_size*10
        self._height=len(self._initial_pattern)*self.tile_size*10

        self.grille=CellSet(self._initial_pattern)
        self.draw_surface= pygame.Surface((self._width,self._height))
        self.screen=pygame.display.set_mode((self._width,self._height))
    
    def display_function(self):
        #on efface la surface à chaque itération
        self.draw_surface.fill((0,0,0))

        for coord in self.grille.dico:
            #on veut afficher que les cellules vivantes qui étaient dans le cadre initial
            x,y=coord
            pygame.draw.rect(self.draw_surface, (255,255,255), pygame.Rect(self.tile_size*y, self.tile_size*x, self.tile_size, self.tile_size))
        
        #quand la nouvelle surface est prête, on l'affiche
        self.screen.blit(self.draw_surface,(0,0))
        pygame.display.update()

    def run(self):

        if self.args.display:
            pygame.init()
            clock = pygame.time.Clock()

        #au cas où on veut s'arrêter avant la fin
        running=True
        while self._current_iter < self._max_iter and running:
            self.grille.calculate_next_state()
            self._current_iter+=1
            #on affiche les clefs du dico ie les coordonnées des cellules vivantes
            #si jamais on affiche la simulation
            if self.args.display:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running=False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running=False
                self.display_function()
                pygame.display.set_caption("Nombre d'étapes : " + str(self._current_iter))
                clock.tick(self._fps)

        #on sauvegarde l'état final 
        self.grille.save_state(self.args.output)

        if self.args.display:
            pygame.quit()  
            quit()

        return self.grille.dico


if __name__ == "__main__":
    # Initialiser les objets nécessaires et exécuter la simulation
    result=Simulation_and_Display().run()
