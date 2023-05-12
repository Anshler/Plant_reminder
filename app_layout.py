from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.config import Config
from kivy.animation import Animation

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

Builder.load_file('layout/MainLayout.kv')


class MainLayout(FloatLayout):
    def open_setting(self):
        print('setting')
    def home_buttons_animation(self,instance):
        if instance.pos_hint != self.ids.home_highlight.pos_hint:
            print(instance.callable_id)
            animate = Animation(pos_hint = instance.pos_hint,duration = .25)
            animate.start(self.ids.home_highlight)



class PlantApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    PlantApp().run()
