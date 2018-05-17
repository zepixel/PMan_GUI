from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

class Main_body(BoxLayout):
    # Corps principal global de l'appli.
    pass


class Main_header(BoxLayout):
    # Barre de header: onglets, info etc.
    pass

class Project_Manager(BoxLayout):
    # Barre laterale de gestion et recherche des projets.
    pass

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
        body = Main_body()
        return body


if __name__== '__main__':
    PmanApp().run()



