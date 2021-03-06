# -*- coding: utf-8 -*-

# imports Project Manager Cli
import os
import xlsconverter
from projectreader import clear, session, project

# imports Kivy
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
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
from kivy.config import Config
from kivy.uix.behaviors import ToggleButtonBehavior


#   Custom Wigets   #
class HeaderTab(ToggleButtonBehavior,BoxLayout):
    TabText = StringProperty("Edit")


#  MAIN BODY  #
class Main_body(BoxLayout):
    # Corps principal global de l'appli.
    pass


class Main_header(BoxLayout):
    # Barre de header: onglets, info etc.

    def use(self):
        print("LOL")
    pass



class Main_Footer(BoxLayout):
    # Pied de page.
    def __init__(self,**kwargs):
        super(Main_Footer,self).__init__(**kwargs)
        Clock.schedule_interval(self.get_session_message,0.1)
        self.appli = App.get_running_app()
    
    def get_session_message(self,dt):
        self.ids["Footer_Label"].text = self.appli.session.message




# LEFT PANEL (project management) #

# Barre laterale de gestion et recherche des projets. Contient Project_Search. et Project_Display.
class Project_Manager(BoxLayout):
    pass
    
# Zone de recherche des projets : contient une icone + SearchBar.
class Project_Search(BoxLayout):
    pass


# Barre de recherche
class SearchBar(TextInput):

    def __init__(self,**kwargs):
        super(SearchBar,self).__init__(**kwargs)
        self.appli= App.get_running_app()
        self.SearchResult =[]      

    def on_text(self,instance, value):
        #print('The widget', instance, 'have:', value)
        self.SearchResult = self.appli.session.Search_Project(value)
        self.parent.parent.ids["ProjectDisplay"].VisibleBtnList = []
        
        clear()
        for projet in self.SearchResult:
            print("\n" , projet)
            self.parent.parent.ids["ProjectDisplay"].VisibleBtnList.append(projet.index)
        print("TERMINE")

        print (self.parent.parent.ids["ProjectDisplay"].VisibleBtnList)




# Custom ToggleButton Class for projects
class ProjectButton(ToggleButton):
    
    def __init__(self,**kwargs):
        super(ProjectButton,self).__init__(**kwargs)
        self.isVisible = True



# Lieu d'affichage des boutons de selection de projets.
class Project_Display(StackLayout):

    def __init__(self,**kwargs):
        # Super init et construction
        super(Project_Display,self).__init__(**kwargs)
        self.size_hint_y=(None)
        self.bind(minimum_height=self.setter('height'))

        self.ProjectBtnList = [] # Liste des boutons de projet
        self.VisibleBtnList =[] # Liste des boutons visibles

        # Liste des projets résultats de la barre de recherche.
        self.SearchResult = []

        # Recupération de l'appli principale
        self.appli= App.get_running_app()
        self.project_list = self.appli.session.project_list

        # Horloge
        self.button_list_constructor()
        Clock.schedule_interval(self.update,0.01)



    def button_list_constructor(self):

        for i,project in enumerate(self.project_list):
            project_btn = ProjectButton(text=project.name, size_hint_y=None, height=80)
            project_btn.id= str(i)
            project_btn.bind(on_press =lambda x:self.attribute_current_project(x,x.id))
            self.ProjectBtnList.append(project_btn)
        
        for i,b in enumerate(self.ProjectBtnList):
            self.add_widget(self.ProjectBtnList[i])

        # Dynamic class IDs dict completion
        self.ids = {child.id:child for child in self.children}



    # Clock Update
    def update(self,dt):
        self.highlight_current_project_button()
        self.set_button_visibility()
        self.hide_buttons()
    

    def attribute_current_project(self,Btn, Btn_id):
        self.appli.session.current_project = self.project_list[int(Btn_id)]
        print (self.appli.session.current_project)
        self.appli.session.current_project.print()
        #status = self.root.ids.StatusBoxLayout.ids.status  https://stackoverflow.com/questions/43450700/kivy-python-how-to-access-to-an-external-child-class-from-the-root-class-face

    # Et c'est ici que ça merde.
        #self.appli.root.ids.Project_name_label.text = self.appli.session.current_project.name
        #self.ids.Edit_Screen.ids.Project_name_label.text = self.appli.session.current_project.name
        #self.ids.Project_students_label.text = ", ".join(self.appli.session.current_project.members)
        #self.ids.Project_path_label.text = self.appli.session.current_project.group
        #self.ids.mark_input.text = self.appli.session.current_project.mark
        #self.ids.comm_input.text = self.appli.session.current_project.comm



        return


    def set_button_visibility(self):
        for id in self.ids:
            if int(self.ids[id].id) in self.VisibleBtnList:
                self.ids[id].isVisible = True
            else:
                self.ids[id].isVisible = False             



    # Current project highlight button
    def highlight_current_project_button(self):
        for id in self.ids:
            if id == str(self.appli.session.current_project.index):
                self.ids[id].state= "down"
            else:
                self.ids[id].state= "normal"


    def hide_buttons(self):
        for id in self.ids:
            if self.ids[id].isVisible == False:
                self.hide_widget(self.ids[id],True)
            else:
                self.hide_widget(self.ids[id],False)


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
        #Clock.schedule_interval(self.update, 0.1)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


    # Clock Callback
    def update(self,dt):
        self.check_current_project()


    def check_current_project(self):
        self.ids.Project_name_label.text = self.appli.session.current_project.name
        self.ids.Project_students_label.text = ", ".join(self.appli.session.current_project.members)
        self.ids.Project_path_label.text = self.appli.session.current_project.group
        self.ids.mark_input.text = self.appli.session.current_project.mark
        self.ids.comm_input.text = self.appli.session.current_project.comm


    def select_previous_project(self):
        self.appli.session.select_previous_result_project()


    def select_next_project(self):
        self.appli.session.select_next_result_project()


    # Keyboard init
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    # Keyboard event
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.select_previous_project()

        elif keycode[1] == 'right':
            self.select_next_project()

        elif keycode[1] == 'up':
            self.select_previous_project()

        elif keycode[1] == 'down':
            self.select_next_project()

        return True





#  MAIN APP  #

class PmanApp(App):
    # main app.

    Window.borderless = False
    Config.set('graphics', 'resizable', 'False')


    def build(self):
                
        self.session = session("session 0","./session/session.json" )
        self.session.load_projects()
        self.session.current_project= self.session.project_list[0]

        # UI 
        self.body = Main_body()
        
        return self.body


if __name__== '__main__':
    PmanApp().run()



