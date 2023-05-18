from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.config import Config
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, SwapTransition
from kivy.core.audio import SoundLoader
from utils.dict_encoding import HomeButtons2Num
from utils.config import *
from utils.format_check import isPasswordFormat,isUsernameFormat
from utils.validation import *
from utils.had_startup import ReadHadStartup,WriteHadStartUp
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
    def home_buttons_animation(self, instance): # animation for home buttons
        if HomeButtons2Num[instance.name] != self.parent.Previous_home_buttons:
            animate = Animation(pos_hint=instance.pos_hint, duration=0.1)
            animate.start(self.ids.home_highlight)
            self.parent.ids.main_pages.transition.duration = 0.2
            # move left/right depend on previous button position
            if HomeButtons2Num[instance.name] > self.parent.Previous_home_buttons:
                self.parent.ids.main_pages.transition.direction = 'left'
            else:
                self.parent.ids.main_pages.transition.direction = 'right'
            # Change screen when press those buttons
            self.parent.ids.main_pages.current = instance.name+'_page'
            self.parent.Previous_home_buttons = HomeButtons2Num[instance.name]

class MasterScreen(Screen):
    Previous_home_buttons = 0
    def swipe_home_buttons(self, instance):
        print('swipe')
    pass

class StartUp(Screen):
    def on_kv_post(self, *args):
        animate = Animation(duration=1)+Animation(color = (1,1,1,1),duration=2)+Animation(duration=2)
        animate.start(self.ids.logo)
        animate.bind(on_complete = self.to_next)
    def to_next(self, *args):
        self.parent.transition = FadeTransition()
        if ReadHadStartup():
            self.parent.current = 'login_screen'
        else:
            self.parent.current = 'sign_up_screen'
class LoginScreen(Screen):
    def on_enter(self, *args):
        self.parent.transition = SlideTransition()
    def press_login_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.login_button_image)
        self.ids.login_button_image.source = 'layout/img/login_pressed.png'
    def login(self,instance): # Expand button and validate
        # Make api call
        # request function()
        isUser = False
        if isUsernameFormat(self.ids.username.text) and isUsernameFormat(self.ids.password.text):
            isUser = simple_login_validation(self.ids.username.text.lower(),self.ids.password.text)

        animate = Animation(width=instance.width, height=instance.height, disabled = False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.login_button_image)
        self.ids.login_button_image.source = 'layout/img/login.png'

        if isUser: # Validated
            # reset these fields
            self.ids.username.text = ''
            self.ids.password.text = ''
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'up'
            self.parent.current = 'master_screen'
        else:
            # if validation failed
            animate = Animation(color = MDApp.get_running_app().wrong_pass_warn,
                                duration=0.2)+Animation(duration=1)+Animation(color = (0,0,0,0),duration=0.5)
            animate.start(self.ids.wrong)

    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled = True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'login_google':
            change_size.start(self.ids.login_google_image)
        elif instance.name == 'login_facebook':
            change_size.start(self.ids.login_facebook_image)
        elif instance.name == 'forget_password':
            change_size.start(self.ids.forget_password_image)
            instance.color = MDApp.get_running_app().press_word_button
        else: # sign up
            change_size.start(self.ids.sign_up_image)
            instance.color = MDApp.get_running_app().press_word_button
    def release_button(self,instance):
        change_size = Animation(duration=0.5) + Animation(width=instance.width, height=instance.height, disabled = False,
                                                      center_x=instance.center_x, center_y=instance.center_y,
                                                      duration=0.01)
        change_color = Animation(duration=0.5)

        # Google login--------------------------------------
        if instance.name == 'login_google':
            change_size.start(self.ids.login_google_image)
            print('login google')

        # Facebook login------------------------------------
        elif instance.name == 'login_facebook':
            change_size.start(self.ids.login_facebook_image)
            print('login facebook')

        # Forget password-----------------------------------
        elif instance.name == 'forget_password':
            change_size.start(self.ids.forget_password_image)
            change_color += Animation(color=MDApp.get_running_app().secondary_font_color, duration=0.1)
            change_color.start(instance)
            # reset these fields
            self.ids.username.text = ''
            self.ids.password.text = ''
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'left'
            self.parent.current = 'forget_password_email_screen'

        # Sign up-------------------------------------------
        else:
            change_size.start(self.ids.sign_up_image)
            change_color += Animation(color=MDApp.get_running_app().primary_font_color, duration=0.1)
            change_color.start(instance)
            # reset these fields
            self.ids.username.text = ''
            self.ids.password.text = ''
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'right'
            self.parent.current = 'sign_up_screen'
class ForgetPasswordEmailScreen(Screen):
    def press_next_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.next_forget_button_image)
        self.ids.next_forget_button_image.source = 'layout/img/login_pressed.png'
    def to_otp(self,instance):
        # Send the request to server to notify
        # request function()
        isUser = False
        if isUsernameFormat(self.ids.email_forget.text):
            isUser = simple_email_validation(self.ids.email_forget.text)

        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.next_forget_button_image)
        self.ids.next_forget_button_image.source = 'layout/img/login.png'
        if isUser: # Validated
            get_otp()
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'left'
            self.parent.current = 'forget_password_otp_screen'
        else:
            # Validation failed
            animate = Animation(color=MDApp.get_running_app().wrong_pass_warn,
                                duration=0.2) + Animation(duration=1) + Animation(color=(0, 0, 0, 0), duration=0.5)
            animate.start(self.ids.wrong_email)
    def press_back(self,instance): # Back button
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
    def release_back(self,instance):
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
        closest_screen = self
        while True:
            if isinstance(closest_screen,Screen):
                # Check if current instance is screen, if not, got back till it is screen
                # It must be screen so we can call screenmanager(the screen's parent) to change screen
                self.parent.transition.duration = 0.5
                self.parent.transition.direction = 'right'
                self.parent.current = 'login_screen'
                break
            else: closest_screen = closest_screen.parent

class ForgetPasswordOTPScreen(Screen):
    def press_confirm_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_otp_button_image)
        self.ids.confirm_otp_button_image.source = 'layout/img/login_pressed.png'
    def to_new_pass(self,instance):
        # Send the request to server to notify
        # request function()
        otp = str(self.ids.otp_pass1.text + self.ids.otp_pass2.text + self.ids.otp_pass3.text + \
              self.ids.otp_pass4.text + self.ids.otp_pass5.text + self.ids.otp_pass6.text)
        isOTP = simple_otp_validation(otp)
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_otp_button_image)
        self.ids.confirm_otp_button_image.source = 'layout/img/login.png'
        if isOTP:
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'left'
            self.parent.current = 'forget_password_new_pass_screen'
        else:
            # Validation failed
            animate = Animation(color=MDApp.get_running_app().wrong_pass_warn,
                                duration=0.2) + Animation(duration=1) + Animation(color=(0, 0, 0, 0), duration=0.5)
            animate.start(self.ids.wrong_otp)
    def press_button(self,instance):
        change_size = Animation(disabled=True)
        change_size.start(self.ids.resend_code_image)
        instance.color = MDApp.get_running_app().press_word_button
    def release_button(self,instance):
        change_size = Animation(disabled=False)
        change_size.start(self.ids.resend_code_image)
        change_color = Animation(duration=0.5) + Animation(color=MDApp.get_running_app().primary_font_color,
                                                           duration=0.1)
        change_color.start(instance)
        # Make api call to resend code
        # request function()
        get_otp()
    def press_back(self,instance):
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
    def release_back(self,instance):
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
        closest_screen = self
        while True:
            if isinstance(closest_screen,Screen):
                self.parent.transition.duration = 0.5
                self.parent.transition.direction = 'right'
                self.parent.current = 'forget_password_email_screen'
                break
            else: closest_screen = closest_screen.parent

class ForgetPasswordNewPassScreen(Screen):
    def press_confirm_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_new_pass_button_image)
        self.ids.confirm_new_pass_button_image.source = 'layout/img/login_pressed.png'
    def login(self,instance): # Expand button and validate
        email = self.parent.ids.forget_password_email_screen.ids.email_forget.text
        isNew = False
        if not isPasswordFormat(self.ids.new_password.text):
            self.ids.wrong.text = 'password must be at least 8 characters,\n contain numbers and capital letters'
        else:
            self.ids.wrong.text = 'new password must be different from old'
            # Make api call
            # request function()
            isNew = simple_password_validation(email, self.ids.new_password.text)

        animate = Animation(width=instance.width, height=instance.height, disabled = False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_new_pass_button_image)
        self.ids.confirm_new_pass_button_image.source = 'layout/img/login.png'
        if isNew:
            # reset all these fields
            self.parent.ids.forget_password_email_screen.ids.email_forget.text = ''
            self.ids.new_password.text = ''
            self.ids.new_password2.text = ''
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'up'
            self.parent.current = 'master_screen'
        else:
            animate = Animation(color = MDApp.get_running_app().wrong_pass_warn,
                                duration=0.2)+Animation(duration=2)+Animation(color = (0,0,0,0),duration=0.5)
            animate.start(self.ids.wrong)
class SignUpScreen(Screen):
    def on_enter(self, *args):
        self.parent.transition = SlideTransition()
    def press_signup_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.sign_up_button_image)
        self.ids.sign_up_button_image.source = 'layout/img/login_pressed.png'
    def signup(self,instance): # Expand button and validate
        isNewUser = False
        if not isUsernameFormat(self.ids.username_sign_up.text):
            self.ids.wrong.text = 'username is insufficient'
        elif not simple_new_user_validation(self.ids.username_sign_up.text):
            self.ids.wrong.text = 'username already exist'
        elif not isUsernameFormat(self.ids.email_sign_up.text):
            self.ids.wrong.text = 'email is insufficient'
        elif not simple_new_email_validation(self.ids.email_sign_up.text):
            self.ids.wrong.text = 'an account with this email already existed'
        elif not isPasswordFormat(self.ids.password_sign_up.text):
            self.ids.wrong.text = 'password must be at least 8 characters,\n contain numbers and capital letters'
        else:
            isNewUser = True

        animate = Animation(width=instance.width, height=instance.height, disabled = False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.sign_up_button_image)
        self.ids.sign_up_button_image.source = 'layout/img/login.png'

        if isNewUser: # Validated
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'left'
            self.parent.current = 'sign_up_otp_screen'

            # Send info with api call
            # request function()
            get_otp()
        else:
            # if validation failed
            animate = Animation(color = MDApp.get_running_app().wrong_pass_warn,
                                duration=0.2)+Animation(duration=1)+Animation(color = (0,0,0,0),duration=0.5)
            animate.start(self.ids.wrong)
    def press_button(self, instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'login_google':
            change_size.start(self.ids.login_google_image)
        elif instance.name == 'login_facebook':
            change_size.start(self.ids.login_facebook_image)
        else:  # sign in
            change_size.start(self.ids.sign_in_image)
            instance.color = MDApp.get_running_app().press_word_button

    def release_button(self, instance):
        change_size = Animation(duration=0.5) + Animation(width=instance.width, height=instance.height, disabled=False,
                                                          center_x=instance.center_x, center_y=instance.center_y,
                                                          duration=0.01)
        change_color = Animation(duration=0.5)

        # Google login--------------------------------------
        if instance.name == 'login_google':
            change_size.start(self.ids.login_google_image)
            print('login google')

        # Facebook login------------------------------------
        elif instance.name == 'login_facebook':
            change_size.start(self.ids.login_facebook_image)
            print('login facebook')

        # Sign in------------------------------------------
        else:
            change_size.start(self.ids.sign_in_image)
            change_color += Animation(color=MDApp.get_running_app().primary_font_color, duration=0.1)
            change_color.start(instance)
            # reset all these fields
            self.ids.username_sign_up.text = ''
            self.ids.email_sign_up.text = ''
            self.ids.password_sign_up.text = ''
            self.ids.password_sign_up2.text = ''
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'left'
            self.parent.current = 'login_screen'
class SignUpOTPScreen(Screen):
    def press_confirm_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_otp_button_image)
        self.ids.confirm_otp_button_image.source = 'layout/img/login_pressed.png'
    def to_master_screen(self,instance):
        # Send the request to server to notify
        # request function()
        otp = str(self.ids.otp_pass1.text + self.ids.otp_pass2.text + self.ids.otp_pass3.text + \
              self.ids.otp_pass4.text + self.ids.otp_pass5.text + self.ids.otp_pass6.text)
        isOTP = simple_otp_validation(otp)
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_otp_button_image)
        self.ids.confirm_otp_button_image.source = 'layout/img/login.png'
        if isOTP:
            simple_signup_vadilation(self.parent.ids.sign_up_screen.ids.username_sign_up.text,
                                     self.parent.ids.sign_up_screen.ids.email_sign_up.text,
                                     self.parent.ids.sign_up_screen.ids.password_sign_up.text)
            # set startup status
            WriteHadStartUp()
            # reset all these fields
            self.parent.ids.sign_up_screen.ids.username_sign_up.text = ''
            self.parent.ids.sign_up_screen.ids.email_sign_up.text = ''
            self.parent.ids.sign_up_screen.ids.password_sign_up.text = ''
            self.parent.ids.sign_up_screen.ids.password_sign_up2.text = ''
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'up'
            self.parent.current = 'master_screen'
        else:
            # Validation failed
            animate = Animation(color=MDApp.get_running_app().wrong_pass_warn,
                                duration=0.2) + Animation(duration=1) + Animation(color=(0, 0, 0, 0), duration=0.5)
            animate.start(self.ids.wrong_otp)
    def press_button(self,instance):
        change_size = Animation(disabled=True)
        change_size.start(self.ids.resend_code_image)
        instance.color = MDApp.get_running_app().press_word_button
    def release_button(self,instance):
        change_size = Animation(disabled=False)
        change_size.start(self.ids.resend_code_image)
        change_color = Animation(duration=0.5) + Animation(color=MDApp.get_running_app().primary_font_color,
                                                           duration=0.1)
        change_color.start(instance)
        # Make api call to resend code
        # request function()
        get_otp()
    def press_back(self,instance):
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
    def release_back(self,instance):
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
        closest_screen = self
        while True:
            if isinstance(closest_screen,Screen):
                self.parent.transition.duration = 0.5
                self.parent.transition.direction = 'right'
                self.parent.current = 'sign_up_screen'
                break
            else: closest_screen = closest_screen.parent
class WindowManager(ScreenManager):
    pass

class PlantApp(MDApp):

    theme = theme
    language = language
    volume = volume
    def play_sound(self, filename):
        sound = SoundLoader.load('soundfx/'+filename)
        if sound:
            sound.volume = self.volume
            sound.play()

    def build(self):
        self.primary_font_color = theme_list[self.theme]['primary_font_color']
        self.secondary_font_color = theme_list[self.theme]['secondary_font_color']
        self.background_color = theme_list[self.theme]['background_color']
        self.wrong_pass_warn = theme_list[self.theme]['wrong_pass_warn']
        self.press_word_button = theme_list[self.theme]['press_word_button']
        kv = Builder.load_file('layout/MainLayout.kv')
        return kv


if __name__ == '__main__':
    PlantApp().run()
