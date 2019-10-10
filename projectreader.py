import os
import json
import re
from xlsconverter import xlsx_doc, web_renderer


def clear():
    os.system('cls' if os.name=='nt' else 'clear')



class project:

    def __init__(self):
        self.name = ""
        self.filepath = ""
        self.members = []
        self.group = ""
        self.mark = "Aucune"
        self.comm = "Aucun commentaire"

        self.tag= []
        self.checksum = False
        self.index = 0


    def print(self):
        # Affichage d'un seul projet.
        print(self.name, "réalisé par", ", ".join(self.members), "en section", self.group, "\n" , "NOTE: ", self.mark,"\nCommentaire: ", self.comm)
        #input("")



# Session : saving , loading, resuming, searching, editing projects
class session:
    
    def __init__(self, name, output):
        # Session
        self.name = name
        self.session_file = output
        self.project_list = []
        self.SearchResult = []
        self.message = ""

        # Projets
        self.project_dir = "./projets"
        self.current_project = project()

        # Nomenclature
        self.class_separator = "_"
        self.members_separator = "-"
        self.project_separator = "."



    # -------- Session -------

    def is_existing(self):
    # Si fichier de sauvegarde de session existant : verifier son contenu.
        if os.path.isfile(self.session_file):
    # Si fichier de sauvegarde de session vide :
            if os.stat(self.session_file).st_size == 0:  
                return False
            else:
                return True
        else :
            return False


    def create_folder(self):
        if not os.path.exists("./session"):
            os.makedirs("./session")
        self.choix_session = 2


    def save(self):
        with open(self.session_file,"w+") as fichier:
            json.dump(self.project_list, fichier,indent=2)		
        print("\nSession sauvegardée\n")


    def load(self):
        with open(self.session_file,"r+") as fichier:
            self.project_list = json.load(fichier)
        input("\nSession chargée. Appuyez sur une touche pour continuer.\n")
        return(self.project_list)


    # -------- Projects -------

    # Chargement des fichiers projets et stockage dans les structures de donnees.
    def load_projects(self):
        
        project_members_list =[]
        fichiers=[fichier for fichier in os.listdir(self.project_dir)]

        for index,fichier in enumerate(fichiers):
            
            project_members_list = fichier.split(self.class_separator)[1]
            project_members_list = project_members_list.split(self.members_separator)

            loading_project = project()

            loading_project.name = fichier.split(self.class_separator)[2]
            loading_project.members = project_members_list
            loading_project.group = fichier.split(self.class_separator)[0]
            loading_project.filepath = fichier
            loading_project.index = index

            self.project_list.append(loading_project)
            
        self.message = "Projets chargés: "+ str(len(self.project_list))


    def print_project_list(self):   
        for project in self.project_list:
            project.print()
            print("\n")


    def select_next_project(self):
        if self.current_project.index != (len(self.project_list) - 1):
            self.current_project = self.project_list[self.current_project.index + 1]
            print("OK")

    def select_previous_project(self):
        if self.current_project.index != 0:
            self.current_project = self.project_list[self.current_project.index -1]
            print("OK")


    def select_previous_result_project(self):
        if self.current_project == self.SearchResult[0]:
            print("MEME PROJET")
            print(int(self.current_project.index))
        else:
            self.current_project = self.SearchResult[self.SearchResult.index(self.current_project)-1]
            print("OK")


    def select_next_result_project(self):
        if self.SearchResult.index(self.current_project) != len(self.SearchResult) - 1:
            self.current_project = self.SearchResult[self.SearchResult.index(self.current_project)+1]
            print("OK")
            
        else:
            print("MEME PROJET")
            print(int(self.current_project.index))
            


    def Search_Project(self, KeyWord):
        self.SearchResult = []
        keyword = KeyWord
        for projet in self.project_list:
            if re.match(keyword, projet.name) != None:
                self.SearchResult.append(projet)
                continue

            #if re.match(keyword, [etudiants for etudiants in projet["ETUDIANTS"]]) == None:
            #   continue

            if re.match(keyword, projet.group) != None:
                self.SearchResult.append(projet)
                continue
                         
            else:
                continue

        self.SearchResult= self.SearchResult
        self.current_project = self.SearchResult[0]

        return self.SearchResult



# PROJECT HANDLER : Put project files into handlable structures.
class project_handler:


    def print_txt_file(self, txt_file, liste_projets):
        with open(txt_file,"w+") as _txt_:
            for projet in liste_projets:
                buffer = "\n\n" + projet["NOM"] + " réalisé par " + ", ".join(projet["ETUDIANTS"]) + ", en section " + projet["SECTION"] +":\n    NOTE: " + projet["NOTE"] + "\n    Commentaire: " + projet["COMMENTAIRE"] + "\n\n"
                _txt_.write(buffer)

        input("\nFichier Evaluations.txt enregistré dans le dossier Sorties.")
