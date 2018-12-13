import os
import json
import re
from xlsconverter import xlsx_doc, web_renderer


def clear():
    os.system('cls' if os.name=='nt' else 'clear')



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Session : saving , loading, resuming, editing projects
class session:
    
    def __init__(self, name, output):
        self.name = name
        self.session_file = output
        self.project_list = []
        self.handler_0 = project_handler()
        self.current_project = 0
        self.message = ""
        self.SearchResult = []


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


    def select_next_project(self):

        if self.current_project["INDEX"] != (len(self.project_list) - 1):
            
            self.current_project = self.project_list[self.current_project["INDEX"]+1]
            print("OK")


    def select_previous_project(self):

        if self.current_project["INDEX"] != 0:
            
            self.current_project = self.project_list[self.current_project["INDEX"]-1]
            print("OK")




# PROJECT HANDLER : Put project files into handlable structures.
class project_handler:

    def __init__(self):
        #self.dir=input("Entrez le chemin d'accès du dossier de projets:\n> ")
        self.dir = "./projets"
        self.projet = {"NOM" : "", "ETUDIANTS": [] , "SECTION" : "","FICHIER" : "", "NOTE": "Aucune note", "COMMENTAIRE" : "Aucun commentaire", "CHECKSUM": 0, "INDEX": 0}

    # Chargement des fichiers projets et stockage dans les structures de donnees.
    def load_projects(self,session):
        
        session.project_list = []
        liste_etudiant_projet =[]
        fichiers=[fichier for fichier in os.listdir(self.dir)]

        for index,fichier in enumerate(fichiers):
            
            liste_etudiant_projet = fichier.split("_")[1]
            liste_etudiant_projet = liste_etudiant_projet.split("-")
        
            self.projet["NOM"] = fichier.split("_")[2]
            self.projet["ETUDIANTS"] = liste_etudiant_projet
            self.projet["SECTION"] = fichier.split("_")[0]
            self.projet["FICHIER"] = fichier
            self.projet["INDEX"]= index
            session.project_list.append(self.projet.copy())
            
        session.message = "Projets chargés: "+ str(len(session.project_list))
        return session.project_list


    # Affichage de la structure globale.
    def print_project_list(self,liste_projets):   
        for projet in liste_projets:
            self.print_project(projet)


    # Affichage d'un seul projet.
    def print_project(self,projet):   
            print(projet["NOM"], "réalisé par", ", ".join(projet["ETUDIANTS"]), "en section", projet["SECTION"], "\n" , "NOTE: ", projet["NOTE"],"\nCommentaire: ", projet["COMMENTAIRE"])
            input("")


    def eval_project(self,projet):
        
        etudiant_eval = "\nEvaluer le projet de: "
        for etudiants in projet["ETUDIANTS"]:
            etudiant_eval = etudiant_eval + etudiants + ", "
            
        etudiant_eval = etudiant_eval + "en section " + projet["SECTION"] + ":\n"
        print(etudiant_eval)
        projet["NOTE"] = input("    NOTE ? >> ")
        projet["COMMENTAIRE"] = input("    COMMENTAIRE ? >> ")
        projet["CHECKSUM"] = 1
        
        return(projet)


    def eval_all_projects(self,session): # Lance l'evaluation des projets, et retourne la liste mise à jour.
        for projet in session.project_list:
            projet = self.eval_project(projet)
            session.save()
        return session.project_list

        
    def resume_eval(self,session):
        for projet in session.project_list:
            if projet["CHECKSUM"] == 1:
                continue
            else:
                projet = self.eval_project(projet)
                session.save()
        input("\nTout les projets ont étés évalués.")
        return(session.project_list)


    def print_txt_file(self, txt_file, liste_projets):
        with open(txt_file,"w+") as _txt_:
            for projet in liste_projets:
                buffer = "\n\n" + projet["NOM"] + " réalisé par " + ", ".join(projet["ETUDIANTS"]) + ", en section " + projet["SECTION"] +":\n    NOTE: " + projet["NOTE"] + "\n    Commentaire: " + projet["COMMENTAIRE"] + "\n\n"
                _txt_.write(buffer)

        input("\nFichier Evaluations.txt enregistré dans le dossier Sorties.")



    def Search_Project(self, session, KeyWord):

        self.SearchResult = []
        keyword = KeyWord

        for projet in session.project_list:

            if re.match(keyword, projet["NOM"]) != None:
                self.SearchResult.append(projet)
                continue

            #if re.match(keyword, [etudiants for etudiants in projet["ETUDIANTS"]]) == None:
            #   continue

            if re.match(keyword, projet["SECTION"]) != None:
                self.SearchResult.append(projet)
                continue
                
            
            else:
                continue

        session.SearchResult= self.SearchResult
        return self.SearchResult