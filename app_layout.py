from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.config import Config
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

homeButtons2num = {'home':0, 'plant_profile':1,'calendar':2,'community':3,'wiki':4,'shopping':5}

# Declare Main pages ----------------------------------------
class HomePage(Screen):
    pass
class PlantProfilePage(Screen):
    pass
class CalendarPage(Screen):
    pass
class CommunityPage(Screen):
    pass
class WikiPage(Screen):
    pass
class ShoppingPage(Screen):
    pass

class MainPagesManager(ScreenManager):
    pass
class UltilityBars(FloatLayout):
    def open_setting(self, instance):
        print('setting')

    def home_buttons_animation(self, instance):
        if homeButtons2num[instance.name] != self.parent.Previous_home_buttons:
            animate = Animation(pos_hint=instance.pos_hint, duration=.25)
            animate.start(self.ids.home_highlight)
            for a in range(len(self.parent.children)): # Can't call ids from parent (dun kno why), so iterate instead
                if self.parent.children[a].name == 'main_pages':
                    self.parent.children[a].current = instance.name
                    if homeButtons2num[instance.name] > self.parent.Previous_home_buttons:
                        self.parent.children[a].transition.direction = 'left'
                    else:
                        self.parent.children[a].transition.direction = 'right'

                    self.parent.Previous_home_buttons = homeButtons2num[instance.name]
                    break
class MasterScreen(FloatLayout):
    Previous_home_buttons = 0
    pass

kv = Builder.load_file('layout/MainLayout.kv')
class PlantApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    PlantApp().run()
