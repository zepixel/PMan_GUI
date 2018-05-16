from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout


class Main_header(BoxLayout):
    pass


class Main_body(BoxLayout):
    pass

class PmanApp(App):
    
    def build(self):
        body = Main_body()

        return body


if __name__== '__main__':
    PmanApp().run()



