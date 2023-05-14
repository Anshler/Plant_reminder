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
from utils.dict_encoding import HomeButtons2Num

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

# Declare Main pages ----------------------------------------
class HomePage(Screen):
    def test(self,instance):
        print('home page')
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
class UtilityBars(FloatLayout):
    def open_setting(self, instance):
        print('setting')
    def home_buttons_animation(self, instance):
        if HomeButtons2Num[instance.name] != self.parent.Previous_home_buttons:
            animate = Animation(pos_hint=instance.pos_hint, duration=0.1)
            animate.start(self.ids.home_highlight)
            self.parent.ids.main_pages.transition.duration = 0.2
            if HomeButtons2Num[instance.name] > self.parent.Previous_home_buttons:
                self.parent.ids.main_pages.transition.direction = 'left'
            else:
                self.parent.ids.main_pages.transition.direction = 'right'
            self.parent.ids.main_pages.current = instance.name
            self.parent.Previous_home_buttons = HomeButtons2Num[instance.name]

class MasterScreen(FloatLayout):
    Previous_home_buttons = 0
    def swipe_home_buttons(self, instance):
        print('swipe')
    pass

kv = Builder.load_file('layout/MainLayout.kv')
class PlantApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    PlantApp().run()
