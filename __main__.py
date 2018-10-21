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
from kivy.event import EventDispatcher


class Main_body(BoxLayout):
    # Corps principal global de l'appli.
    pass


class Main_header(BoxLayout):
    # Barre de header: onglets, info etc.
    pass


class Main_SM(ScreenManager):
    # ScreenManager pour switcher de eval a render.
    pass

class Project_Manager(BoxLayout):
    # Barre laterale de gestion et recherche des projets. Contient Project_Search. et Project_Display.
    pass

class Project_Search(BoxLayout):
    # Zone de recherche des projets.
    pass


class Project_Display(StackLayout):
# Lieu d'affichage des objets projets.

    def __init__(self,**kwargs):

    # Init
        self.ProjectBtnList = []
        self.appli= App.get_running_app()
        self.project_list = self.appli.session_0.project_list
        
        super(Project_Display,self).__init__(**kwargs)
        self.size_hint_y=(None)
        self.bind(minimum_height=self.setter('height'))

        
    # Button List constructor
        for i,project in enumerate(self.project_list):
            project_btn = Button(text=project["NOM"], size_hint_y=None, height=80)
            project_btn.id= str(i)
            project_btn.bind(on_press =lambda x:self.btnlbl(x,x.id))
            self.ProjectBtnList.append(project_btn)


        for i,b in  enumerate(self.ProjectBtnList):
            self.add_widget(self.ProjectBtnList[i])



    def btnlbl(self,Btn, labl):
        Btn.text = labl
        return



class Eval_Screen(Screen):
    # Ecran d'évaluation des projets.
    pass


#class Project_Eval(EventDispatcher):

#    def __init__(self,session)




class Main_Footer(BoxLayout):
    # Pied de page.
    pass


class PmanApp(App):
    # main app.
    Window.borderless = True

    
    def build(self):
        
        # Project Handler
        self.session_0 = session("session 0","./session/session.json" )
        self.session_0.handler_0.load_projects(self.session_0)

        # UI 
        self.body = Main_body()
        return self.body


if __name__== '__main__':
    PmanApp().run()



