# -*- coding: utf-8 -*-

# imports Project Manager Cli
import os
import xlsconverter
from projectreader import clear, session, project_handler

# imports Kivy
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.event import EventDispatcher


#  MAIN BODY  #

class Main_body(BoxLayout):
    # Corps principal global de l'appli.
    pass


class Main_header(BoxLayout):
    # Barre de header: onglets, info etc.
    pass



class Main_Footer(BoxLayout):
    # Pied de page.
    pass





# LEFT PANEL (project management) #

class Project_Manager(BoxLayout):
    # Barre laterale de gestion et recherche des projets. Contient Project_Search. et Project_Display.
    pass

class Project_Search(BoxLayout):
    # Zone de recherche des projets.
    pass



class Project_Display(StackLayout):
# Lieu d'affichage des objets projets.

    def __init__(self,**kwargs):

        # Liste des boutons de projet
        self.ProjectBtnList = []
        self.DisplayBtnList =[]
        # Recupération de l'appli principale
        self.appli= App.get_running_app()
        # Stockage de la liste des projets de la session vers une liste locale
        self.project_list = self.appli.session_0.project_list
        
        # Super init et construction
        super(Project_Display,self).__init__(**kwargs)
        self.size_hint_y=(None)
        self.bind(minimum_height=self.setter('height'))

        Clock.schedule_once(self.button_list_constructor)
        Clock.schedule_interval(self.button_list_update,0.01)


    def attribute_current_project(self,Btn, Btn_id):

        self.appli.session_0.current_project = self.project_list[int(Btn_id)]
        print (self.appli.session_0.current_project)


        return


    def button_list_constructor(self,dt):

        for i,project in enumerate(self.project_list):
            project_btn = ToggleButton(text=project["NOM"], size_hint_y=None, height=80)
            project_btn.id= str(i)
            project_btn.bind(on_press =lambda x:self.attribute_current_project(x,x.id))
            self.ProjectBtnList.append(project_btn)
        
        for i,b in enumerate(self.ProjectBtnList):
            self.add_widget(self.ProjectBtnList[i])


        # Dynamic class IDs dict completion
        self.ids = {child.id:child for child in self.children}


    def button_list_update(self,dt):

        #self.hide_widget(self.ids["2"],True)
        #self.hide_widget(self.ids["2"],False)


        # Current project highlight button
        for id in self.ids:
            if id == str(self.appli.session_0.current_project["INDEX"]):
                self.ids[id].state= "down"
            else:
                self.ids[id].state= "normal"




    # from Matteljay / stackoverflow
    def hide_widget(self,wid, dohide=True):
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True






# RIGHT PANEL (project editing) #

# ScreenManager pour switcher de Edit a Render.
class Main_SM(ScreenManager):
    
    pass


# Ecran d'évaluation des projets.
class Edit_Screen(Screen):

    def __init__(self,**kwargs):
        super(Edit_Screen,self).__init__(**kwargs)
        self.appli= App.get_running_app()
        Clock.schedule_interval(self.check_current_project, 0.1)

    # Clock Callback
    def check_current_project(self,dt):
        #print("clock")

        self.ids.Project_name_label.text = self.appli.session_0.current_project["NOM"]
        self.ids.Project_students_label.text = ", ".join(self.appli.session_0.current_project["ETUDIANTS"])
        self.ids.Project_path_label.text = self.appli.session_0.current_project["FICHIER"]


    def select_previous_project(self):
        self.appli.session_0.select_previous_project()


    def select_next_project(self):
        self.appli.session_0.select_next_project()



#  MAIN APP  #

class PmanApp(App):
    # main app.
    Window.borderless = True

    
    def build(self):
        
        # Project Handler
        self.session_0 = session("session 0","./session/session.json" )
        self.session_0.handler_0.load_projects(self.session_0)
        self.session_0.current_project= self.session_0.project_list[0]

        # UI 
        self.body = Main_body()
        return self.body


if __name__== '__main__':
    PmanApp().run()



