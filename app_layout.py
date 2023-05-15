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
        if username == '' or password == '':
            print('can\'t login')
            for a in range(0,50000000):
                b=1
            return False
        try:
            # This would be an api call
            for a in range(0, 50000000):
                b = 1
            auth = [json.loads(a) for a in open('placeholder_server/user/user.json', encoding='utf-8')]
            for user in auth:
                if user['username'].lower() == username and user['password'] == password:
                    return True
                if user['gmail'].lower() == username and user['password'] == password:
                    return True
        except: pass
        for a in range(0, 50000000):
            b = 1
        print('can\'t login')
        return False
    def press_login_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.login_button_image)
        self.ids.login_button_image.source = 'layout/img/login_pressed.png'
    def login(self,instance): # Expand button and validate
        isUser = self.__simple_validation(self.ids.username.text.lower(),self.ids.password.text)
        animate = Animation(width=instance.width, height=instance.height, disabled = False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.login_button_image)
        self.ids.login_button_image.source = 'layout/img/login.png'
        if isUser:
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'up'
            self.parent.current = 'master_screen'
        else:
            animate = Animation(color = (208/255, 0, 0,1),duration=0.2)+Animation(duration=1)+Animation(color = (0,0,0,0),duration=0.5)
            animate.start(self.ids.wrong)

    def press_button(self,instance):
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'login_google':
            animate.start(self.ids.login_google_image)
        elif instance.name == 'login_facebook':
            animate.start(self.ids.login_facebook_image)
        else:
            instance.color = (1, 1, 110 / 255, 1)
        instance.disabled = True


    def release_button(self,instance):
        animate = Animation(duration=0.5) + Animation(width=instance.width, height=instance.height,
                                                      center_x=instance.center_x, center_y=instance.center_y,
                                                      duration=0.01)
        animate2 = Animation(duration=0.5)
        if instance.name == 'login_google':
            animate.start(self.ids.login_google_image)
            print('login google')
        elif instance.name == 'login_facebook':
            animate.start(self.ids.login_facebook_image)
            print('login facebook')
        elif instance.name == 'forget_password':
            animate2 += Animation(color=self.ids.welcome2.color, duration=0.1)
            animate2.start(instance)
            print('forget password')
        else:
            animate2 += Animation(color=self.ids.welcome.color, duration=0.1)
            animate2.start(instance)
            print('signup')
        instance.disabled=False
class WindowManager(ScreenManager):
    pass

class PlantApp(MDApp):
    def build(self):
        kv = Builder.load_file('layout/MainLayout.kv')
        return kv


if __name__ == '__main__':
    PlantApp().run()
