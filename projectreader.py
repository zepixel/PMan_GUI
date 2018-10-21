import os
import json
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


class session:
    
    def __init__(self, name, output):
        self.name = name
        self.session_file = output
        self.project_list = []
        self.handler_0 = project_handler()
    

    def is_existing(self):
              
        # Si fichier de sauvegarde de session existant : verifier son contenu.
        if os.path.isfile(self.session_file):
            # Si fichier de sauvegarde de session vide : FALSE
            if os.stat(self.session_file).st_size == 0:  
                return False
            else:
                return True
        else:
            return False



    def create(self):
            
        if not os.path.exists("./session"):
            os.makedirs("./session")


    def save(self):
        with open(self.session_file,"w+") as fichier:
            json.dump(self.project_list, fichier,indent=2)		
        print("\nSession sauvegardée\n")


    def load(self):
        with open(self.session_file,"r+") as fichier:
            self.project_list = json.load(fichier)
        input("\nSession chargée. Appuyez sur une touche pour continuer.\n")
        return(self.project_list)



   


class project_handler:

    def __init__(self):
        #self.dir=input("Entrez le chemin d'accès du dossier de projets:\n> ")
        self.dir = "./projets"
        self.projet = {"NOM" : "", "ETUDIANTS": [] , "SECTION" : "","FICHIER" : "", "NOTE": "Aucune note", "COMMENTAIRE" : "Aucun commentaire", "CHECKSUM": 0}


    def load_projects(self,session): # Chargement des fichiers projets et stockage dans les structures de donnees.
        
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
            session.project_list.append(self.projet.copy())
            
        print("Projets charges :", len(session.project_list))
        return session.project_list


    def print_project_list(self,liste_projets):   
        for projet in liste_projets:
            self.print_project(projet)

            
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


    def find_project(self,session):
        while True:
            clear()
            try:
                choix = int(input('''Quelle recherche souhaitez vous effectuer ?
        
        1. Rechercher par nom.
        2. Rechercher par section.
        3. Rechercher par note.
        4. Rechercher par commentaire.
        5. Retour.
        
    >> '''))
                break
            except ValueError:
                input("\nEntrez un numéro de menu valide.")



        if choix == 1:
            clear()
            resultats =[]
            recherche = input("Entrez le nom de l'etudiant que vous recherchez.\n\n>> ")
                
            for projet in session.project_list:
                for etudiant in projet["ETUDIANTS"]:
                    
                    if etudiant != recherche:
                        continue
                    else:
                        if projet in resultats:
                            break
                        else:
                            resultats.append(projet)
                    
            if resultats:
                print(len(resultats) , " projets trouvé(s) :\n")

                for index, resultat in enumerate(resultats):
                    
                    print("    " + str(index+1) + ".", resultat["SECTION"] +":", end=" " )
                    for nom in resultat["ETUDIANTS"]:
                        if nom != recherche:
                            print(nom, end=", ")
                        else:
                            print(bcolors.OKBLUE + nom + bcolors.ENDC, end=", ")

                    print( "\n        NOTE: " + resultat["NOTE"] , "\n        COMMENTAIRE:", resultat["COMMENTAIRE"],"\n")
                print("    0. Retour\n")

                
                while True:
                    try:
                        selection_index = int(input("Entrez votre selection >> "))
                        break
                    except ValueError:
                        input("\nEntrez un numéro de menu valide.")    
                print("")


                if selection_index !=0:
                    self.print_project(resultats[selection_index - 1])
                    
                    while True:
                    
                        try:
                            choix_2 = int(input("\nQue souhaitez vous faire ?\n1. Réevaluer le projet ?\n2. Retour\n>> "))
                            break
                        except ValueError:
                            input("\nEntrez un numéro de menu valide.")
            
                    if choix_2 == 1:
                        self.eval_project(resultats[selection_index - 1])
                        session.save()
                
                else:
                    pass
                
            if resultats == []:                
                input("\nAucun projet trouvé.")
            else:
                input("\nFin de la recherche")

    
    
    
        if choix == 2:
            clear()
            resultats = []
            recherche = input("Entrez le nom de la section que vous recherchez.\n\n>> ")
            
            for projet in session.project_list:
                if projet["SECTION"] != recherche:
                    continue
                else:
                    if projet in resultats:
                        break
                    else:
                        resultats.append(projet)  
            if resultats:
                print(len(resultats) , " projets trouvé(s) :\n")
                for index, resultat in enumerate(resultats):
                    print("    " + str(index+1) + ".", bcolors.OKBLUE + resultat["SECTION"] +bcolors.ENDC +":", ", ".join(resultat["ETUDIANTS"]), "\n        NOTE: " + resultat["NOTE"], "\n        COMMENTAIRE:", resultat["COMMENTAIRE"],"\n")

                while True:
                    try:
                        selection_index = int(input(" Choisissez un projet >> ")) - 1
                        break
                    except ValueError:
                        input("\nEntrez un numéro de menu valide.")

                print("")
                self.print_project(resultats[selection_index])
                choix_2 = int(input("\nQue souhaitez vous faire ?\n1. Réevaluer le projet ?\n2. Retour\n>> "))
        
                if choix_2 == 1:
                    self.eval_project(resultats[selection_index])
                    session.save()


                            
            if resultats == []:                
                input("\nAucun projet trouvé.")
            else:
                input("\nFin de la recherche")


        if choix == 3:
            clear()
            resultats = []
            recherche = input("Entrez la note que vous recherchez.\n\n>> ")
            
            for projet in session.project_list:
                if projet["NOTE"] != recherche:
                    continue
                else:
                    if projet in resultats:
                        break
                    else:
                        resultats.append(projet)


            if resultats:
                print(len(resultats) , " projets trouvé(s) :\n")
                for index, resultat in enumerate(resultats):
                    print("    " + str(index+1) + ".", resultat["SECTION"] +":", ", ".join(resultat["ETUDIANTS"]), "\n        NOTE: " + bcolors.OKBLUE + resultat["NOTE"] + bcolors.ENDC, "\n        COMMENTAIRE:", resultat["COMMENTAIRE"],"\n")

                while True:
                    try:
                        selection_index = int(input(" Choisissez un projet >> ")) - 1
                        break
                    except ValueError:
                        input("\nEntrez un numéro de menu valide.")

                print("")
                self.print_project(resultats[selection_index])
                choix_2 = int(input("\nQue souhaitez vous faire ?\n1. Réevaluer le projet ?\n2. Retour\n>> "))
        
                if choix_2 == 1:
                    self.eval_project(resultats[selection_index])
                    session.save()


            if resultats == []:                
                input("\nAucun projet trouvé.")
            else:
                input("\nFin de la recherche")

        if choix == 4:
            clear()
            resultats = []
            recherche = input("Entrez le commentaire que vous recherchez.\n\n>> ")
            
            for projet in session.project_list:
                for word in projet["COMMENTAIRE"].split():
                    if word != recherche:
                        continue
                    else:
                        if projet in resultats:
                            break
                        else:
                            resultats.append(projet)

            if resultats:
                print(len(resultats) , " projets trouvé(s) :\n")
                for index, resultat in enumerate(resultats):
                    print("    " + str(index+1) + ".", resultat["SECTION"] +":", ", ".join(resultat["ETUDIANTS"]), "\n        COMMENTAIRE:", end=" ")
                    for word in resultat["COMMENTAIRE"].split():
                        if word != recherche:
                            print(word, end=" ")
                        else:
                            print(bcolors.OKBLUE + word + bcolors.ENDC, end=" ")

                    print("\n")

                while True:
                    try:
                        selection_index = int(input(" Choisissez un projet >> ")) - 1
                        break
                    except ValueError:
                        input("\nEntrez un numéro de menu valide.")

                print("")
                while True:

                    try:
                        clear()
                        self.print_project(resultats[selection_index])
                        choix_2 = int(input("\nQue souhaitez vous faire ?\n1. Réevaluer le projet ?\n2. Retour\n>> "))
                        if choix_2 == 1:
                            self.eval_project(resultats[selection_index])
                            session.save()

                        break
                    except ValueError:
                        input("\nEntrez un numéro de menu valide.")
            
            if resultats == []:                
                input("\nAucun projet trouvé.")
            else:
                input("\nFin de la recherche")
