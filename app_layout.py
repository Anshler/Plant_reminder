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
import json,time


Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '700')

from kivymd.app import MDApp

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

class MasterScreen(Screen):
    Previous_home_buttons = 0
    def swipe_home_buttons(self, instance):
        print('swipe')
    pass
class LoginScreen(Screen):
    def __simple_validation(self,username,password):
        time.sleep(1)
        if username == '' or password == '':
            print('can\'t login')
            return False
        try:
            # This would be an api call
            auth = [json.loads(a) for a in open('placeholder_server/user/user.json', encoding='utf-8')]
            for user in auth:
                if user['username'].lower() == username and user['password'] == password:
                    return True
                if user['gmail'].lower() == username and user['password'] == password:
                    return True
        except: pass
        print('can\'t login')
        return False
    def press_login_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.login_button_image)
        self.ids.login_button_image.source = 'layout/img/login_pressed.png'
    def login(self,instance): # Expand button and validate
        isUser = self.__simple_validation(self.ids.username.text.lower(),self.ids.password.text)
        animate = Animation(width=instance.width, height=instance.height,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.login_button_image)
        self.ids.login_button_image.source = 'layout/img/login.png'
        if isUser:
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'up'
            self.parent.current = 'master_screen'
        else:
            animate = Animation(color = (208/255, 0, 0,1),duration=0.2)+Animation(duration=1)+Animation(color = (0,0,0,0),duration=1)
            animate.start(self.ids.wrong)

    def press_button(self,instance):
        instance.color = (1,1,110/255,1)
    def release_button(self, instance):
        if instance.name == 'forget_password':
            print('forget password')
            instance.color = (124/255, 130/255, 161/255,1)
        else:
            print('signup')
            instance.color = (51 / 255, 54 / 255, 71 / 255, 1)

    def press_other_login(self,instance):
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'login_google':
            animate.start(self.ids.login_google_image)
        else:
            animate.start(self.ids.login_facebook_image)

    def release_other_login(self,instance):
        animate = Animation(width=instance.width, height=instance.height,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'login_google':
            print('login google')
            animate.start(self.ids.login_google_image)
        else:
            print('login facebook')
            animate.start(self.ids.login_facebook_image)
class WindowManager(ScreenManager):
    pass

class PlantApp(MDApp):
    def build(self):
        kv = Builder.load_file('layout/MainLayout.kv')
        return kv


if __name__ == '__main__':
    PlantApp().run()
