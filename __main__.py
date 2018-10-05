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

        # Project Button List
        self.ProjectBtnList = []

        super(Project_Display,self).__init__(**kwargs)
        self.size_hint_y=(None)
        self.bind(minimum_height=self.setter('height'))

        
        # Button List constructor
        
        for i in range(3):
            btn = Button(text=str(i), size_hint_y=None, height=80)
            btn.id= str(i)
            btn.text= "lol"
            btn.bind(on_press =lambda x:self.btnlbl(x,x.id))
            self.ProjectBtnList.append(btn)


        for i,b in  enumerate(self.ProjectBtnList):
            self.add_widget(self.ProjectBtnList[i])


    def btnlbl(self,Btn, labl):
        Btn.text = labl
        return



class Eval_Screen(Screen):
    # Ecran d'évaluation des projets.
    pass



class Main_Footer(BoxLayout):
    # Pied de page.
    pass


class PmanApp(App):
    # main app.
    Window.borderless = True

    
    def build(self):
        
        # Project Handler
        print("lol")
        self.session_0 = session("session 0","./session/session.json" )
        #self.session_0.selection()
        #self.session_0.run()


        # UI 
        self.body = Main_body()
        return self.body


if __name__== '__main__':
    PmanApp().run()



