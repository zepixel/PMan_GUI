from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class main_body(Widget):
    pass

class PmanApp(App):
    
    def build(self):
        body = main_body()

        return body


if __name__== '__main__':
    PmanApp().run()



