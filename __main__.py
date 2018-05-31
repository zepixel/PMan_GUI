# -*- coding: utf-8 -*-

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
        super(Project_Display,self).__init__(**kwargs)
        self.size_hint_y=(None)
        self.bind(minimum_height=self.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=80)
            btn.id= str(i)
            btn.text= btn.id
            self.add_widget(btn)



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
        self.body = Main_body()
        return self.body


if __name__== '__main__':
    PmanApp().run()



