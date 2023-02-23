from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

Builder.load_file('layout/MainLayout.kv')


class MainLayout(FloatLayout):
    pass


class PlantApp(App):
    def build(self):

        return MainLayout()


if __name__ == '__main__':
    PlantApp().run()
