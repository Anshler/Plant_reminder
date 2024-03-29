from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, CardTransition, NoTransition
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors.touchripple import TouchRippleButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.factory import Factory
from kivy.config import Config
from functools import partial

from kivy.utils import platform
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])
from utils.dict_encoding import *
from utils.random_color import *
from utils.config import *
from utils.dict_filter import *
from utils.format_check import isPasswordFormat, isUsernameFormat
from utils.validation import *
from utils.plant_profile_management import *
from utils.had_startup import *
from utils.EncyclopediaCrawler import *
from utils.transaction import *
from virtual_pet.gpt3 import get_chatgpt_assistant, get_chatgpt_classifier, get_chatgpt_calendar
from virtual_pet.chatbot import chat_with_plant_gpt

if platform == 'android':
    Config.set('graphics', 'fullscreen', 'auto')
Config.set('kivy', 'window_icon', get_file_path('layout/img/logo.png'))
Config.set('graphics', 'window_state', 'maximized')
Config.set('kivy','pause_on_minimize', 1)

from kivy.uix.relativelayout import RelativeLayout
import kivymd.uix.relativelayout
from kivy_gradient import Gradient
from kivymd.icon_definitions import md_icons
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.uix.behaviors import CommonElevationBehavior

# Declare Main pages ----------------------------------------
class TestPage(Screen):
    pass

class NotificationButton(TouchRippleButtonBehavior,FloatLayout):
    def to_calendar(self,instance):
        if self.task != 'No task':
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = self.callable_id
            day = Day2DayRev[self.day]
        else:
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = 'none_filter'
            day = None
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.change_day(day=day)
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.to_calendar()
class HomePage(Screen):
    def on_pre_enter(self, *args):
        self.ids.scroll_view.scroll_y = 1
    def update_time(self,*args):
        MDApp.get_running_app().now = datetime.datetime.now().strftime('%H:%M')
        self.ids.current_time.text = MDApp.get_running_app().now
        MDApp.get_running_app().today = datetime.datetime.today().strftime('%A, %d %B')
        self.ids.current_date.text = MDApp.get_running_app().today

    def get_next_event(self, *args):
        calendar = MDApp.get_running_app().calendar_full
        # Initialize variables to store the closest event and its time distance
        closest_event = None
        closest_date_range = None
        closest_day = None
        closest_time = None
        closest_time_distance = None

        found = False

        if calendar is not None and calendar != {}:
            # Get the current datetime.datetime
            now = datetime.datetime.now()
            # Iterate over each date range in the calendar
            for date_range in calendar:
                if found:
                    break
                # Parse the start and end dates from the date range
                start_date, end_date = map(datetime.datetime.fromisoformat, date_range.split('_'))

                # Check if the current datetime.datetime is within the date range
                if start_date <= now <= end_date:
                    # Iterate over the events in the current date range
                    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                    for day in day_list:
                        if found:
                            break
                        events = calendar[date_range][day]
                        day_date = start_date + datetime.timedelta(days=Days2Num[day])
                        # Iterate over the events in each day
                        for time, event in events.items():
                            # Parse the event time
                            event_time = datetime.datetime.combine(day_date,
                                                                   datetime.datetime.strptime(time, '%H:%M').time())
                            now_minute = now.replace(second=0, microsecond=0)
                            if event_time >= now_minute:
                                # Calculate the time difference between the next event and the current time
                                if event_time == now_minute:
                                    time_difference = 'Now'
                                else: time_difference = event_time - now

                                # Check if the current event is the closest event so far
                                closest_event = event
                                closest_date_range = date_range
                                closest_day = day
                                closest_time = time
                                closest_time_distance = time_difference

                                found = True
                                break


        if closest_event is not None:
            # assign the closest values
            if type(closest_time_distance) is not str:
                if closest_time_distance.days > 0:
                    # If there are days present, format the timedelta as X day HH:MM:SS
                    closest_time_distance = f"{closest_time_distance.days} day"
                else:
                    # If there are no days, format the timedelta as HH:MM:SS
                    closest_time_distance = f"{closest_time_distance.seconds // 3600:02d}h {(closest_time_distance.seconds // 60) % 60:02d}m {closest_time_distance.seconds % 60:02d}s"

            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.time_remain = str(closest_time_distance).split(',')[0]
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.task = closest_event[0]['task']
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.callable_id = closest_event[0]['callable_id']
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.name = closest_event[0]['name']
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.day = closest_day
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.represent_color = closest_event[0]['represent_color']
            if MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.avatar != MDApp.get_running_app().plant_list[closest_event[0]['callable_id']]['avatar']:
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.avatar = \
                MDApp.get_running_app().plant_list[closest_event[0]['callable_id']]['avatar']
            task_avatar = 'layout/img/'+ closest_event[0]['task']+'.png'
            if MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.task_avatar != task_avatar:
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.task_avatar = task_avatar
        else:
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.time_remain = 'You\'re free this week!'
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.task = 'No task'
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.callable_id = ''
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.name = ''
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.day = ''
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.represent_color = MDApp.get_running_app().primary_font_color
            if MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.avatar != 'layout/img/default_plant_avatar.png':
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.avatar = 'layout/img/default_plant_avatar.png'
            if MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.task_avatar != 'layout/img/emoticon-outline.png':
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.home_page.ids.next_event.task_avatar = 'layout/img/emoticon-outline.png'

    def to_calendar(self):
        animate = Animation(
            pos_hint=MDApp.get_running_app().root.ids.master_screen.ids.utility_bars.ids.calendar.pos_hint,
            duration=0.1)
        animate.start(MDApp.get_running_app().root.ids.master_screen.ids.utility_bars.ids.home_highlight)
        MDApp.get_running_app().root.ids.master_screen.Previous_home_buttons = 2
        self.parent.transition = SlideTransition()
        self.parent.transition.duration = 0.25
        self.parent.transition.direction = 'left'
        self.parent.current = 'calendar_page'
class PlantSelector(FloatLayout):
    def press_button(self,instance):
        instance.disabled = True
        instance.background_color = (0.5,0.5,0.5,0.25)
    def release_button(self,instance):
        instance.disabled = False
        animate = Animation(duration = 0.1)+Animation(duration=0.1, background_color=(0,0,0,0))
        animate.start(instance)
    def open_item(self,instance):
        # disable the buttons
        self.parent.parent.parent.parent.parent.parent.parent.ids.filter_button.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.search_bar.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.search_button.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.normal_button.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.chat_button.disabled = True

        #update
        self.parent.parent.parent.parent.parent.parent.parent.current_plant = self.callable_id
        self.parent.parent.parent.parent.parent.parent.parent.plant_name = self.name
        self.parent.parent.parent.parent.parent.parent.parent.location = self.location
        self.parent.parent.parent.parent.parent.parent.parent.date_added = self.date_added
        self.parent.parent.parent.parent.parent.parent.parent.represent_color = self.represent_color
        # change screen
        self.parent.parent.parent.parent.parent.parent.transition = CardTransition()
        self.parent.parent.parent.parent.parent.parent.transition.mode = 'push'
        self.parent.parent.parent.parent.parent.parent.transition.duration = 0.5
        self.parent.parent.parent.parent.parent.parent.transition.direction = 'left'
        self.parent.parent.parent.parent.parent.parent.current = 'plant_screen'
class PlantChatSelector(FloatLayout):
    def press_button(self,instance):
        instance.disabled = True
        instance.background_color = (0.5,0.5,0.5,0.25)
    def release_button(self,instance):
        instance.disabled = False
        animate = Animation(duration = 0.1)+Animation(duration=0.1, background_color=(0,0,0,0))
        animate.start(instance)
    def open_item(self,instance):
        # disable the buttons
        self.parent.parent.parent.parent.parent.parent.parent.ids.filter_button.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.search_bar.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.search_button.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.normal_button.disabled = True
        self.parent.parent.parent.parent.parent.parent.parent.ids.chat_button.disabled = True

        #update
        if self.parent.parent.parent.parent.parent.parent.parent.current_plant_chat != self.callable_id:
            self.parent.parent.parent.parent.parent.parent.parent.different_plant = True
            self.parent.parent.parent.parent.parent.parent.parent.current_plant_chat = self.callable_id
        else:
            self.parent.parent.parent.parent.parent.parent.parent.different_plant = False
        self.parent.parent.parent.parent.parent.parent.parent.plant_name = self.name
        self.parent.parent.parent.parent.parent.parent.parent.date_added = self.date_added
        self.parent.parent.parent.parent.parent.parent.parent.represent_color = self.represent_color
        # change screen
        self.parent.parent.parent.parent.parent.parent.transition = CardTransition()
        self.parent.parent.parent.parent.parent.parent.transition.mode = 'push'
        self.parent.parent.parent.parent.parent.parent.transition.duration = 0.5
        self.parent.parent.parent.parent.parent.parent.transition.direction = 'left'
        self.parent.parent.parent.parent.parent.parent.current = 'plant_chat_screen'
class PlantScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.scroll_view.scroll_y = 1
        result = MDApp.get_running_app().plant_list_advanced[self.parent.parent.current_plant]
        basic_info = ''
        basic_info+= '• Plant\'s name: '+self.parent.parent.plant_name+'\n• Date added: '+self.parent.parent.date_added+'\n• Owner\'s location: '
        if self.parent.parent.location == '':
            basic_info += 'Not given'
        else:
            basic_info += self.parent.parent.location

        self.ids.basic_info.text = basic_info
        self.ids.represent_color_image.color = self.parent.parent.represent_color
        self.ids.overview.text = '• ' + result['Overview'].replace('. ', '\n• ')
        self.ids.water_tip.text = '• '+result['Water'].replace('. ', '\n• ')
        self.ids.light_tip.text = '• '+result['Light'].replace('. ', '\n• ')
        self.ids.humidity_tip.text = '• '+result['Humidity'].replace('. ', '\n• ')
        self.ids.temperature_tip.text = '• '+result['Temperature'].replace('. ', '\n• ')
        self.ids.ph_level_tip.text = '• '+result['PH Level'].replace('. ', '\n• ')
        self.ids.suggested_placement_area_tip.text = '• '+result['Suggested Placement Area'].replace('. ', '\n• ')
        self.ids.others_tip.text = '• '+result['Others'].replace('. ', '\n• ')

    def press_back(self, instance):  # Back button
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)

    def release_back(self, instance):
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
        # re-enable the button
        self.parent.parent.ids.filter_button.disabled = False
        self.parent.parent.ids.search_bar.disabled = False
        self.parent.parent.ids.search_button.disabled = False
        self.parent.parent.ids.normal_button.disabled = False
        self.parent.parent.ids.chat_button.disabled = False

        # change screen
        self.parent.transition.mode = 'pop'
        self.parent.transition.duration = 0.5
        self.parent.transition.direction = 'right'
        self.parent.current = 'profile_display'
    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'view_calendar_button':
            change_size.start(self.ids.view_calendar_button)
        else:
            change_size.start(self.ids.delete_plant)
    def release_button(self,instance):
        change_size = Animation(size_hint=(0.8, 0.4), disabled=False,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'view_calendar_button':
            change_size.start(self.ids.view_calendar_button)
        else:
            change_size.start(self.ids.delete_plant)
    def to_calendar(self,instance):
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = self.parent.parent.current_plant
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.change_day()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.to_calendar()
    def quit_screen(self):
        # re-enable the button
        self.parent.parent.ids.filter_button.disabled = False
        self.parent.parent.ids.search_bar.disabled = False
        self.parent.parent.ids.search_button.disabled = False
        self.parent.parent.ids.normal_button.disabled = False
        self.parent.parent.ids.chat_button.disabled = False

        # change screen
        self.parent.transition.mode = 'pop'
        self.parent.transition.duration = 0.5
        self.parent.transition.direction = 'right'
        self.parent.current = 'profile_display'
class Message(FloatLayout):
    def update_message_size(self, message, texture_size):
        # when the label is updated, we want to make sure the displayed size is
        # proper

        # if i set max_with to message.with, the long message work but short message failed
        # if i set it to window's width, the short message work but long message failed
        # honestly, i don't understand this max_width part, but it works if I alternate between them
        max_width = message.width
        if max_width == 0:
            max_width = Window.size[0]
        one_line = Window.size[1]  # a bit of  hack, YMMV
        # if the texture is too big, limit its size
        if texture_size[0] >= max_width * 2 / 3:
            message.text_size = (max_width * 2 / 3, None)

        # if it was limited, but is now too small to be limited, raise the limit
        elif texture_size[1] > one_line:
            message.text_size = (max_width * 2 / 3, None)
            message._size = texture_size
        # just set the size
        else:
            message._size = texture_size
class PlantChatScreen(Screen):
    def on_pre_enter(self, *args):
        current_plant = self.parent.parent.current_plant_chat
        different_plant = self.parent.parent.different_plant
        self.plant_name = MDApp.get_running_app().plant_list[current_plant]['name']
        self.avatar = MDApp.get_running_app().plant_list[current_plant]['avatar']
        self.represent_color = MDApp.get_running_app().plant_list[current_plant]['represent_color']
        self.ids.energy_count.text = MDApp.get_running_app().root.ids.master_screen.ids.energy_count.text

        self.ids.load_legacy_button.disabled = True
        self.ids.load_legacy_button.opacity = 0
        if different_plant:
            self.legacy_index = 0
            self.ids.message_boxlayout.clear_widgets()
    def on_enter(self, *args):
        current_plant = self.parent.parent.current_plant_chat
        different_plant = self.parent.parent.different_plant
        recent_plant_conversation = MDApp.get_running_app().plant_conversation[current_plant]['recent']

        # load conversation
        if different_plant and recent_plant_conversation != []:
            self.ids.message_boxlayout.add_widget(FloatLayout(size_hint = (1,None), height= Window.size[1]*0.05))
            for i in range(0, len(recent_plant_conversation), 3):
                user_input = recent_plant_conversation[i + 1].split('user:')[1]
                message = Message()
                setattr(message, 'text', user_input)
                setattr(message, 'side', 'right')
                self.ids.message_boxlayout.add_widget(message)

                assistant_reply = recent_plant_conversation[i + 2].split('assistant:')[1]
                message = Message()
                setattr(message, 'text', assistant_reply)
                setattr(message, 'side', 'left')
                self.ids.message_boxlayout.add_widget(message)
        self.ids.scroll_view.scroll_y = 0
    def load_legacy_button_display(self, instance):
        show_button = Animation(disabled=False, opacity=1, duration = 0.25)
        hide_button = Animation(disabled=True, opacity=0, duration=0.25)
        if ((self.ids.message_boxlayout.height > instance.height and instance.scroll_y >= 1) or self.ids.message_boxlayout.height <= instance.height) and len(MDApp.get_running_app().plant_conversation[self.parent.parent.current_plant_chat]['legacy']) > self.legacy_index*9:
            show_button.start(self.ids.load_legacy_button)
        else:
            hide_button.start(self.ids.load_legacy_button)
    def load_legacy(self,instance):
        current_plant = self.parent.parent.current_plant_chat
        recent_plant_conversation = MDApp.get_running_app().plant_conversation[current_plant]['recent']
        legacy_plant_conversation = MDApp.get_running_app().plant_conversation[current_plant]['legacy']

        self.ids.message_boxlayout.clear_widgets()
        self.ids.message_boxlayout.add_widget(FloatLayout(size_hint=(1, None), height=Window.size[1] * 0.05))
        # load legacy chat
        index = len(legacy_plant_conversation[-(self.legacy_index+1)*9:])
        for i in range(0, index, 3):
            user_input = legacy_plant_conversation[-index + i + 1].split('user:')[1]
            message = Message()
            setattr(message, 'text', user_input)
            setattr(message, 'side', 'right')
            self.ids.message_boxlayout.add_widget(message)

            assistant_reply = legacy_plant_conversation[-index + i + 2].split('assistant:')[1]
            message = Message()
            setattr(message, 'text', assistant_reply)
            setattr(message, 'side', 'left')
            self.ids.message_boxlayout.add_widget(message)
        # load current chat
        for i in range(0, len(recent_plant_conversation), 3):
            user_input = recent_plant_conversation[i + 1].split('user:')[1]
            message = Message()
            setattr(message, 'text', user_input)
            setattr(message, 'side', 'right')
            self.ids.message_boxlayout.add_widget(message)

            assistant_reply = recent_plant_conversation[i + 2].split('assistant:')[1]
            message = Message()
            setattr(message, 'text', assistant_reply)
            setattr(message, 'side', 'left')
            self.ids.message_boxlayout.add_widget(message)
        self.ids.scroll_view.scroll_y = 0.99
        self.legacy_index += 1
        instance.opacity = 0


    def press_back(self, instance):  # Back button
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)

    def release_back(self, instance):
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.start_filtering(mode='chat')
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
        # re-enable the button
        self.parent.parent.ids.filter_button.disabled = False
        self.parent.parent.ids.search_bar.disabled = False
        self.parent.parent.ids.search_button.disabled = False
        self.parent.parent.ids.normal_button.disabled = False
        self.parent.parent.ids.chat_button.disabled = False

        # change screen
        self.parent.transition.mode = 'pop'
        self.parent.transition.duration = 0.5
        self.parent.transition.direction = 'right'
        self.parent.current = 'profile_display'
    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'send_message':
            instance.opacity = 0.5
            change_size.start(self.ids.send_message_image)
        elif instance.name == 'load_legacy_button':
            instance.disabled = True
            self.background_color = MDApp.get_running_app().press_word_button
    def release_button(self,instance):
        change_size = Animation(width=instance.width, height=instance.height, disabled=False,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'send_message':
            instance.opacity = 1
            change_size.start(self.ids.send_message_image)
        elif instance.name == 'load_legacy_button':
            self.background_color = MDApp.get_running_app().secondary_background_color
    def send_message(self,instance):
        user_input = self.ids.chat_input.text.strip()
        if len(user_input) == 0:
            return
        if MDApp.get_running_app().energy >= 1:
            message = Message()
            setattr(message, 'text', user_input)
            setattr(message, 'side', 'right')
            self.ids.message_boxlayout.add_widget(message)
            self.ids.chat_input.text = ''
            self.ids.scroll_view.scroll_y = 0

            Clock.schedule_once(lambda dt: self.get_reply(user_input= user_input), 1.0)
        else:
            Factory.GoPrePopup(
                title='You are low on energy. Purchase more energy or wait to recover').open()

    def get_reply(self,user_input, *args):
        current_username = MDApp.get_running_app().current_username
        current_plant = self.parent.parent.current_plant_chat
        plant_conversation = MDApp.get_running_app().plant_conversation
        MDApp.get_running_app().plant_conversation[current_plant], chat_reply, total_tokens_used = chat_with_plant_gpt(
            user_input=user_input, user=current_username, plant_conversation=plant_conversation[current_plant])

        if chat_reply != '' and chat_reply is not None:
            MDApp.get_running_app().root.ids.master_screen.recalculate(energy= -total_tokens_used)
            save_conversation(MDApp.get_running_app().plant_conversation, MDApp.get_running_app().current_user)

            message = Message()
            setattr(message, 'text', chat_reply)
            setattr(message, 'side', 'left')
            MDApp.get_running_app().play_sound('message.wav')
            self.ids.message_boxlayout.add_widget(message)
            print(total_tokens_used)
        else:
            message = Message()
            setattr(message, 'color', MDApp.get_running_app().wrong_pass_warn)
            setattr(message, 'text', 'Message failed to deliver, please try again later')
            setattr(message, 'side', 'left')
            MDApp.get_running_app().play_sound('message.wav')
            self.ids.message_boxlayout.add_widget(message)
        self.ids.scroll_view.scroll_y = 0


class LineSeparator(FloatLayout):
    pass
class CancelNewPlantPopup(Popup):
    def press_button(self,instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button
    def release_button(self,instance):
        instance.disabled = False
        if instance.text == 'quit':
            instance.color = MDApp.get_running_app().wrong_pass_warn
        else:
            instance.color = MDApp.get_running_app().primary_font_color
    def quit_create(self,instance):
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.quit_screen()
        self.dismiss()
class FailConfirmPopup(Popup):
    pass
class ConfirmNextStepPopup(Popup):
    def press_button(self,instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button
    def release_button(self,instance):
        instance.disabled = False
        if instance.text == 'confirm':
            instance.color = MDApp.get_running_app().wrong_pass_warn
        else:
            instance.color = MDApp.get_running_app().primary_font_color
    def confirm(self,instance):
        name_manual = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.manual_input_text.text.strip()
        toggle = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.toggle_manual.active
        valid = True
        if toggle:
            valid, total_tokens_used = get_chatgpt_classifier(username=MDApp.get_running_app().current_username, prompt=str('plant\'s name: ' + name_manual))
            MDApp.get_running_app().root.ids.master_screen.recalculate(energy=-total_tokens_used)

        if valid:
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.new_plant_step_manager.transition = CardTransition()
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.new_plant_step_manager.transition.mode = 'push'
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.new_plant_step_manager.transition.duration = 0.25
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.new_plant_step_manager.transition.direction = 'left'
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.new_plant_step_manager.current = 'new_plant_step2'
            self.dismiss()
        else:
            self.dismiss()
            Factory.FailConfirmPopup().open()
class PlantCreationSucessfull(Popup):
    def on_pre_open(self):
        self.confirm()
        if MDApp.get_running_app().seed <= 1:
            self.title = 'Plant creation successful! You have %d seed left' % MDApp.get_running_app().seed
        else:
            self.title = 'Plant creation successful! You have %d seeds left' % MDApp.get_running_app().seed
    def confirm(self):
        name_auto = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.specie_detection.strip()
        name_manual = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.manual_input_text.text.strip()
        toggle = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.toggle_manual.active
        represent_color = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.represent_color
        avatar = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.plant_avatar.source
        age = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.age_text.text.strip()
        location = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.location_text.text.strip()
        extra_notes = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.extra_notes_text.text.strip()
        date_added = datetime.datetime.now().strftime("%Y/%m/%d")

        if toggle:
            name = name_manual
        else:
            name = name_auto

        # advanced info
        result = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.new_plant_step2.result
        # add new plant to plant list
        current_user = MDApp.get_running_app().current_user
        simple_add_new_plant(current_user,name,represent_color,avatar,age,date_added,location,extra_notes, result)

        MDApp.get_running_app().plant_list = get_plant_list()
        MDApp.get_running_app().plant_list_advanced = get_plant_list_advanced()
        MDApp.get_running_app().plant_calendar = get_plant_calendar()
        MDApp.get_running_app().plant_conversation = get_plant_conversation()
        # update seed count
        MDApp.get_running_app().root.ids.master_screen.recalculate(seed=-1)
        # reset plant filter
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.last_search = ['','none_filter']
        # update screen
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.update_plant_list()
class ConfirmFinalStepPopup(Popup):
    def on_pre_open(self):
        if MDApp.get_running_app().subscription_status == 'free':
            self.ids.pro_feature_chat.opacity = 1
        else:
            self.ids.pro_feature_chat.opacity = 0

    def press_button(self, instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button

    def release_button(self, instance):
        instance.disabled = False
        if instance.text == 'yes, please':
            instance.color = MDApp.get_running_app().wrong_pass_warn
        else:
            instance.color = MDApp.get_running_app().primary_font_color

    def confirm_manual(self, instance):
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.quit_screen()
        self.dismiss()
    def confirm_auto(self, instance):
        if MDApp.get_running_app().subscription_status != 'free':
            if MDApp.get_running_app().energy >= 1:
                new_plant_id = list(MDApp.get_running_app().plant_list.keys())[-1]
                plant_info = MDApp.get_running_app().plant_list[new_plant_id]
                result = MDApp.get_running_app().plant_list_advanced[new_plant_id]

                # create prompt
                auto_calendar_prompt = 'Plan\'s name: ' + plant_info['name']
                if plant_info['location'].strip() != '':
                    auto_calendar_prompt += '\nOwner\'s location: ' + plant_info['location'].strip()
                if plant_info['extra_notes'].strip() != '':
                    auto_calendar_prompt += '\nOwner\'s request: ' + plant_info['extra_notes'].strip()
                auto_calendar_prompt += '\nJobs to perform:\n' + result['Water'] + '\n' + result['Humidity'] + '\n' + \
                                             result['Others']

                schedule, total_tokens_used = get_chatgpt_calendar(username=MDApp.get_running_app().current_username, prompt=auto_calendar_prompt)
                if total_tokens_used != 0:
                    MDApp.get_running_app().root.ids.master_screen.recalculate(energy=-total_tokens_used)

                    simple_edit_plant_schedule(MDApp.get_running_app().current_user, new_plant_id, schedule)
                    update_calendar(MDApp.get_running_app().current_user)
                    MDApp.get_running_app().calendar_full = get_calendar_full()
                    MDApp.get_running_app().cycle = get_cycle()

                    # filter by id of new plant
                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = new_plant_id

                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.change_day()
                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.quit_screen()
                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.to_calendar()
                    self.dismiss()
                    MDApp.get_running_app().play_sound('sliding.wav')
                else:
                    self.dismiss()
                    Factory.GoPrePopupFromCalendarCreation(
                        title='Failed to create a schedule. Try again later').open()
            else:
                self.dismiss()
                Factory.GoPrePopupFromCalendarCreation(
                    title='You are low on energy. Purchase more energy or wait to recover').open()
        else:
            self.dismiss()
            Factory.GoPrePopupFromCalendarCreation().open()

class DeletePlantPopup(Popup):
    def press_button(self, instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button
    def release_button(self, instance):
        instance.disabled = False
        if instance.text == 'delete':
            instance.color = MDApp.get_running_app().wrong_pass_warn
        else:
            instance.color = MDApp.get_running_app().primary_font_color
    def quit_create(self, instance):
        current_plant = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.current_plant
        current_user = MDApp.get_running_app().current_user

        simple_remove_key_plant_list(current_user, current_plant)
        # update seed count
        MDApp.get_running_app().root.ids.master_screen.recalculate(seed=1)

        MDApp.get_running_app().plant_list = get_plant_list()
        MDApp.get_running_app().plant_list_advanced = get_plant_list_advanced()
        MDApp.get_running_app().plant_calendar = get_plant_calendar()
        MDApp.get_running_app().plant_conversation = get_plant_conversation()

        update_calendar(current_user)
        MDApp.get_running_app().cycle = get_cycle()
        MDApp.get_running_app().calendar_full = get_calendar_full()

        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.update_plant_list()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.current_plant = ''
        # reset if new calendar is empty
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = 'none_filter'
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.change_day()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.plant_screen.quit_screen()
        self.dismiss()
class NewPlantInfoScreen(Screen):
    result = {}
    def on_pre_enter(self, *args):
        self.ids.scroll_view.scroll_y = 1
        prompt = ''
        prompt += 'plant\'s name: '+self.plant_name
        if self.location != '':
            prompt += '\nowner\'s location: ' + self.location

        self.result, total_tokens_used = get_chatgpt_assistant(username=MDApp.get_running_app().current_username, prompt=prompt)
        if total_tokens_used != 0:
            self.ids.confirm_new_plant.disabled = False
            MDApp.get_running_app().root.ids.master_screen.recalculate(energy=-total_tokens_used)
        else:
            self.ids.confirm_new_plant.disabled = True
        self.ids.overview.text = '• ' + self.result['Overview'].replace('. ', '\n• ')
        self.ids.water_tip.text = '• '+self.result['Water'].replace('. ', '\n• ')
        self.ids.light_tip.text = '• '+self.result['Light'].replace('. ', '\n• ')
        self.ids.humidity_tip.text = '• '+self.result['Humidity'].replace('. ', '\n• ')
        self.ids.temperature_tip.text = '• '+self.result['Temperature'].replace('. ', '\n• ')
        self.ids.ph_level_tip.text = '• '+self.result['PH Level'].replace('. ', '\n• ')
        self.ids.suggested_placement_area_tip.text = '• '+self.result['Suggested Placement Area'].replace('. ', '\n• ')
        self.ids.others_tip.text = '• '+self.result['Others'].replace('. ', '\n• ')
    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'confirm_new_plant':
            change_size.start(self.ids.confirm_new_plant)
    def release_button(self,instance):
        change_size = Animation(width=instance.width, height=instance.height, disabled=False,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'confirm_new_plant':
            change_size = Animation(size_hint=(0.8, 0.8), disabled=False,
                                    center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
            change_size.start(self.ids.confirm_new_plant)
class PlantColorPickerPopUp(Popup):
    def on_pre_open(self):
        self.ids.color_picker.color = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.represent_color
    def press_button(self,instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button

    def release_button(self,instance):
        instance.disabled = False
        if instance.text == 'apply':
            instance.color = MDApp.get_running_app().wrong_pass_warn
        else:
            instance.color = MDApp.get_running_app().primary_font_color
    def apply_color(self,instance):
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.represent_color = self.ids.color_picker.color
        self.dismiss()
class YearButton(Button):
    def press_button(self, instance):
        instance.disabled = True
        instance.background_color = MDApp.get_running_app().secondary_background_color

    def release_button(self, instance):
        text = instance.text if instance.text != 'None' else ''
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.ids.age_text.text = text
        self.parent.parent.parent.parent.parent.parent.dismiss()
        instance.disabled = False
        instance.background_color = MDApp.get_running_app().background_color
class PlantYearSelectionPopup(Popup):
    def on_pre_open(self, *args):
        self.ids.scroll_view.scroll_y = 1
        self.ids.year_display.clear_widgets()
        year = datetime.datetime.now().year
        year_box = YearButton(text='None', height=Window.size[1] / 15)
        self.ids.year_display.add_widget(year_box)
        for a in reversed(range(year-100,year+1)):
            year_box = YearButton(text=str(a), height = Window.size[1]/15)
            self.ids.year_display.add_widget(year_box)
class ShadowButton(CommonElevationBehavior,Button):
    pass
class NewPlantScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.new_plant_step_manager.transition.duration = 0
        self.ids.new_plant_step_manager.current = 'new_plant_step1'
        self.ids.scroll_view.scroll_y = 1
        self.represent_color = GetRGBA()
        # name (auto)
        self.specie_detection = ''
        self.ids.plant_avatar.source = 'layout/img/default_plant_avatar.png'
        self.ids.toggle_manual.active = False
        # name (manual)
        self.ids.manual_input_text.text = ''
        # age
        self.ids.age_text.text = ''
        # location
        self.ids.location_text.text = ''
        self.ids.scroll_view_extra.scroll_y = 1
        # extra notes
        self.ids.extra_notes_text.text = ''
    def on_enter(self, *args):
        self.parent.parent.ids.overlay2.background_color = (0,0,0,0.5)
    def press_cancel_button(self,instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button
    def release_cancel_button(self,instance):
        instance.disabled = False
        instance.color = MDApp.get_running_app().wrong_pass_warn
    def quit_screen(self):
        self.parent.parent.ids.overlay2.background_color = (0,0,0,0)
        self.parent.transition.mode = 'pop'
        self.parent.transition.duration = 0.25
        self.parent.transition.direction = 'down'
        self.parent.current = 'profile_display'

    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'plant_avatar_picker':
            change_size.start(self.ids.plant_avatar_picker_image)
        elif instance.name == 'plant_color_picker':
            change_size.start(self.ids.plant_color_picker_image)
        elif instance.name == 'set_age':
            change_size.start(self.ids.set_age_image)
        else:
            change_size.start(self.ids.generate_new_plant)
    def release_button(self,instance):
        change_size = Animation(width=instance.width, height=instance.height, disabled=False,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'plant_avatar_picker':
            change_size.start(self.ids.plant_avatar_picker_image)
        elif instance.name == 'plant_color_picker':
            change_size.start(self.ids.plant_color_picker_image)
        elif instance.name == 'set_age':
            change_size.start(self.ids.set_age_image)
        else:
            change_size = Animation(size_hint=(0.8, 0.8), disabled=False,
                                    center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
            change_size.start(self.ids.generate_new_plant)
class FilterScreenProfile(Screen):
    def change_filter(self,instance):
        self.ids.none_filter.background_color = (0,0,0,0)
        self.ids.A_Z_filter.background_color = (0, 0, 0, 0)
        self.ids.Z_A_filter.background_color = (0, 0, 0, 0)
        self.ids.oldest.background_color = (0, 0, 0, 0)
        instance.background_color = MDApp.get_running_app().background_color
    def shut_selector(self,instance):
        self.parent.parent.parent.parent.ids.filter_button.content = instance.content
        self.parent.transition.direction = 'up'
        self.parent.transition.duration = 0.2
        self.parent.current = 'filter_null'

class GoPrePopup(Popup):
    def press_button(self,instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button
    def release_button(self,instance):
        instance.disabled = False
        if instance.text == 'cancel':
            instance.color = MDApp.get_running_app().primary_font_color
        else:
            instance.color = MDApp.get_running_app().wrong_pass_warn
    def to_dismiss(self):
        self.dismiss()
    def to_shopping(self):
        self.dismiss()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.to_shopping()
class GoPrePopupFromCalendarCreation(GoPrePopup):
    def to_dismiss(self):
        self.dismiss()
        Factory.ConfirmFinalStepPopup().open()
    def to_shopping(self):
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.new_plant_screen.quit_screen()
        self.dismiss()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.to_shopping()
class GoPrePopupFromCalendarEdit(GoPrePopup):
    def to_dismiss(self):
        self.dismiss()
        Factory.ConfirmEditCalendarPopup().open()
class PlantProfilePage(Screen):
    last_search = ['','none_filter']
    current_plant = ''
    current_plant_chat = ''
    plant_name = ''
    location = ''
    date_added = ''
    represent_color = [0,0,0,0]

    def add_new_plant(self,instance):
        if MDApp.get_running_app().seed > 0:
            if MDApp.get_running_app().energy >= 1:
                self.ids.overlay.canvas.clear()
                with self.ids.overlay.canvas:
                    Color(0,0,0,0.5)
                    Rectangle(pos=self.pos, size=self.size)
                self.ids.profile_and_add.transition = CardTransition()
                self.ids.profile_and_add.transition.mode = 'push'
                self.ids.profile_and_add.transition.duration = 0.25
                self.ids.profile_and_add.transition.direction = 'up'
                self.ids.profile_and_add.current = 'new_plant_screen'
            else:
                Factory.GoPrePopup(title = 'You are low on energy. Purchase more energy or wait to recover').open()
        else:
            Factory.GoPrePopup(title = 'You ran out of seed! Purchase more seeds, or remove a plant').open()

    def load_filter_selector(self,instance):
        self.ids.filter_selector_manager.transition = SlideTransition()
        self.ids.filter_selector_manager.transition.duration = 0.2
        if self.ids.filter_selector_manager.current == 'filter_null':
            self.ids.filter_selector_manager.transition.direction = 'down'
            self.ids.filter_selector_manager.current = 'filter_select'
        else:
            self.ids.filter_selector_manager.transition.direction = 'up'
            self.ids.filter_selector_manager.current = 'filter_null'
    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled = True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'filter_button':
            change_size.start(self.ids.filter_button_image)
        else:
            change_size.start(self.ids.search_button_image)
    def release_button(self,instance):
        change_size = Animation(width=instance.width, height=instance.height, disabled = False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'filter_button':
            change_size.start(self.ids.filter_button_image)
        else:
            change_size.start(self.ids.search_button_image)

    def start_filtering(self, mode = None):
        sort_filter = self.ids.filter_button.content
        name_filter = self.ids.search_bar.text.strip()

        if [name_filter,sort_filter] == self.last_search:
            if mode is None:
                return
        else: self.last_search = [name_filter,sort_filter]

        filtered_plant_list = MDApp.get_running_app().plant_list
        plant_conversation = MDApp.get_running_app().plant_conversation
        if filtered_plant_list == {} or filtered_plant_list is None:
            return
        if name_filter != '':
            filtered_plant_list = filter_dict_by_column(filtered_plant_list,'name',name_filter)
        if filtered_plant_list != {} and filtered_plant_list is not None and sort_filter != 'none_filter':
            if sort_filter == 'A_Z_filter':
                filtered_plant_list = sort_dict_by_column(filtered_plant_list,'name', reverse=True)
            elif sort_filter == 'Z_A_filter':
                filtered_plant_list = sort_dict_by_column(filtered_plant_list, 'name')
            elif sort_filter == 'recently_added':
                filtered_plant_list = sort_dict_by_column(filtered_plant_list, 'date_added')
            else:
                filtered_plant_list = sort_dict_by_column(filtered_plant_list, 'date_added',reverse=True)

        filtered_plant_conversation = {a:plant_conversation[a] for a in filtered_plant_list}
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.update_plant_list(filtered_plant_list, filtered_plant_conversation)
    def to_calendar(self):
        animate = Animation(
            pos_hint=MDApp.get_running_app().root.ids.master_screen.ids.utility_bars.ids.calendar.pos_hint,
            duration=0.1)
        animate.start(MDApp.get_running_app().root.ids.master_screen.ids.utility_bars.ids.home_highlight)
        MDApp.get_running_app().root.ids.master_screen.Previous_home_buttons = 2
        self.parent.transition = SlideTransition()
        self.parent.transition.duration = 0.25
        self.parent.transition.direction = 'left'
        self.parent.current = 'calendar_page'
    def to_shopping(self):
        animate = Animation(
            pos_hint=MDApp.get_running_app().root.ids.master_screen.ids.utility_bars.ids.shopping.pos_hint,
            duration=0.1)
        animate.start(MDApp.get_running_app().root.ids.master_screen.ids.utility_bars.ids.home_highlight)
        MDApp.get_running_app().root.ids.master_screen.Previous_home_buttons = 5
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.transition = SlideTransition()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.transition.duration = 0.25
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.transition.direction = 'left'
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.current = 'shopping_page'
    def update_plant_list(self, plant_list = None, plant_conversation = None):
        if plant_list is None:
            plant_list = MDApp.get_running_app().plant_list
            plant_conversation = MDApp.get_running_app().plant_conversation
        # update plant profile from anywhere
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_box_scrollview.scroll_y = 1
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_chatbox_scrollview.scroll_y = 1
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_box.clear_widgets()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_chatbox.clear_widgets()

        if plant_list is not None and plant_list == {}:
            available = 'You have no plant'
            if self.last_search != ['','none_filter']:
                available = 'No plant found'
            default_plant = PlantSelector(height=Window.size[1] * 0.1)
            default_plant.ids.default_text.color = (0.5,0.5,0.5,0.5)
            default_plant.ids.default_text.pos_hint = {'center_x': 0.5,'center_y': 0.5}
            default_plant.ids.default_text.size_hint_x = 1
            default_plant.ids.default_text.halign = 'center'
            default_plant.ids.default_text.shorten = False
            default_plant.ids.date_added.text = ''
            setattr(default_plant, 'name', available)
            setattr(default_plant, 'avatar', '')
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_box.add_widget(
                default_plant)

            default_plant = PlantSelector(height=Window.size[1] * 0.1)
            default_plant.ids.default_text.color = (0.5, 0.5, 0.5, 0.5)
            default_plant.ids.default_text.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            default_plant.ids.default_text.size_hint_x = 1
            default_plant.ids.default_text.halign = 'center'
            default_plant.ids.default_text.shorten = False
            default_plant.ids.date_added.text = ''
            setattr(default_plant, 'name', available)
            setattr(default_plant, 'avatar', '')
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_chatbox.add_widget(
                default_plant)
        elif plant_list is not None and plant_list != {}:
            for callable_id in reversed(plant_list):
                default_plant = PlantSelector(height=Window.size[1] * 0.1)
                setattr(default_plant, 'callable_id', callable_id)
                setattr(default_plant, 'name', plant_list[callable_id]['name'])
                setattr(default_plant, 'represent_color', plant_list[callable_id]['represent_color'])
                setattr(default_plant, 'avatar', plant_list[callable_id]['avatar'])
                setattr(default_plant, 'age', plant_list[callable_id]['age'])
                setattr(default_plant, 'location', plant_list[callable_id]['location'])
                setattr(default_plant, 'extra_notes', plant_list[callable_id]['extra_notes'])
                setattr(default_plant, 'date_added', MDApp.get_running_app().plant_list[callable_id]['date_added'])
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_box.add_widget(
                    default_plant)

                default_plant = PlantChatSelector(height=Window.size[1] * 0.1)
                setattr(default_plant, 'callable_id', callable_id)
                setattr(default_plant, 'name', plant_list[callable_id]['name'])
                setattr(default_plant, 'represent_color', plant_list[callable_id]['represent_color'])
                setattr(default_plant, 'avatar', plant_list[callable_id]['avatar'])
                if plant_conversation[callable_id]['recent'] != []:
                    recent = plant_conversation[callable_id]['recent'][-1].split(':',1)[1]
                else:
                    recent = 'Type something to start a conversation'
                setattr(default_plant, 'recent', recent)

                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_chatbox.add_widget(
                    default_plant)
    def change_mode(self,instance):
        mode = instance.name.split('_')[0]
        if MDApp.get_running_app().subscription_status != 'free':
            if self.mode != mode:
                self.mode = mode
                self.ids.normal_and_chat.transition = NoTransition()
                self.ids.normal_and_chat.current = mode+'_profile'
        elif mode == 'chat':
            Factory.GoPrePopup().open()


class HourLayout(FloatLayout):
    pass
class DayLayout(BoxLayout):
    pass
class WeekLayout(BoxLayout):
    pass
class TaskWidget(FloatLayout):
    pass
class EmptyTaskWidget(FloatLayout):
    pass
class HourBoxWidget(FloatLayout):
    pass
class ConfirmEditCalendarPopup(Popup):
    def on_pre_open(self):
        if MDApp.get_running_app().subscription_status == 'free':
            self.ids.pro_feature_chat.opacity = 1
        else:
            self.ids.pro_feature_chat.opacity = 0

    def press_button(self, instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button

    def release_button(self, instance):
        instance.disabled = False
        if instance.text == 'yes, please':
            instance.color = MDApp.get_running_app().wrong_pass_warn
        else:
            instance.color = MDApp.get_running_app().primary_font_color

    def confirm_auto(self):
        if MDApp.get_running_app().subscription_status != 'free':
            if MDApp.get_running_app().energy >= 1:
                # advanced info
                current_user = MDApp.get_running_app().current_user
                plant_id = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content
                plant_info = MDApp.get_running_app().plant_list[plant_id]
                plant_info_advanced = MDApp.get_running_app().plant_list_advanced[plant_id]
                auto_calendar_prompt = 'Plan\'s name: ' + plant_info['name']
                if plant_info['location'].strip() != '':
                    auto_calendar_prompt += '\nOwner\'s location: ' + plant_info['location'].strip()
                if plant_info['extra_notes'].strip() != '':
                    auto_calendar_prompt += '\nOwner\'s request: ' + plant_info['extra_notes'].strip()
                auto_calendar_prompt += '\nJobs to perform:\n' + plant_info_advanced['Water'] + '\n' + \
                                             plant_info_advanced['Humidity'] + '\n' + plant_info_advanced['Others']
                # get schedule
                schedule, total_tokens_used = get_chatgpt_calendar(username=MDApp.get_running_app().current_username, prompt=auto_calendar_prompt)
                if total_tokens_used != 0:
                    MDApp.get_running_app().root.ids.master_screen.recalculate(energy=-total_tokens_used)

                    simple_edit_plant_schedule(current_user, plant_id, schedule)
                    MDApp.get_running_app().plant_calendar = get_plant_calendar()
                    # update calendar full
                    update_calendar(MDApp.get_running_app().current_user)
                    MDApp.get_running_app().calendar_full = get_calendar_full()
                    MDApp.get_running_app().cycle = get_cycle()

                    # update calendar display in calendar page
                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.change_day()
                    MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.scroll_view.scroll_y = 1
                    self.dismiss()
                    MDApp.get_running_app().play_sound('sliding.wav')
                else:
                    self.dismiss()
                    Factory.GoPrePopup(
                        title='Failed to create a schedule. Try again later').open()
            else:
                self.dismiss()
                Factory.GoPrePopupFromCalendarEdit(
                    title='You are low on energy. Purchase more energy or wait to recover').open()
        else:
            self.dismiss()
            Factory.GoPrePopupFromCalendarEdit().open()
class PlantButton(ButtonBehavior, FloatLayout):
    def press_button(self,instance):
        for a in range (len(self.parent.children)):
            self.parent.children[a].background_color = MDApp.get_running_app().background_color
        self.background_color = MDApp.get_running_app().secondary_background_color
    def release_button(self,instance):
        # set_filter
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = self.callable_id
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.change_day()

        self.parent.parent.parent.parent.parent.parent.dismiss()
        if self.callable_id != 'none_filter' and isinstance(self.parent.parent.parent.parent.parent.parent,PickCalendarFilterForEditPopup):
            Factory.ConfirmEditCalendarPopup().open()

class PickCalendarFilterPopup(Popup):
    def on_pre_open(self, *args):
        self.ids.scroll_view.scroll_y = 1
        self.ids.year_display.clear_widgets()
        year = datetime.datetime.now().year
        year_box = PlantButton(height=Window.size[1] / 15)
        if year_box.callable_id == MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content:
            setattr(year_box, 'background_color', MDApp.get_running_app().secondary_background_color)
        self.ids.year_display.add_widget(year_box)
        plant_list = MDApp.get_running_app().plant_list
        for a in reversed(plant_list):
            year_box = PlantButton(height=Window.size[1] / 15)
            setattr(year_box,'name',plant_list[a]['name'])
            setattr(year_box, 'represent_color', plant_list[a]['represent_color'])
            setattr(year_box, 'callable_id', a)
            if year_box.callable_id == MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content:
                setattr(year_box, 'background_color', MDApp.get_running_app().secondary_background_color)
            self.ids.year_display.add_widget(year_box)
class PickCalendarFilterForEditPopup(PickCalendarFilterPopup):
    pass
class CalendarPage(Screen):
    def on_pre_enter(self, *args):
        self.ids.scroll_view.scroll_y = 1
    def reset_calendar(self,*args):
        day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        hour_list = ['0', '4', '8', '12', '16', '20']
        for day in day_list:
            for hour in hour_list:
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.week.ids[day].ids[
                    hour].ids.hour_box.clear_widgets()
    def update_cycle(self,*args):
        cycle = MDApp.get_running_app().cycle
        current_week_range = MDApp.get_running_app().current_week_range
        calendar_week_range = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.current_week
        if cycle is not None and cycle != {} and cycle['start_cycle'] < cycle['end_cycle']:
            now = datetime.datetime.now().date()
            if now > MDApp.get_running_app().cycle['end_cycle']:
                update_calendar(MDApp.get_running_app().current_user)
                MDApp.get_running_app().cycle = get_cycle()
                MDApp.get_running_app().calendar_full = get_calendar_full()
            if current_week_range is not None and calendar_week_range != current_week_range:
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.current_week = current_week_range
                current_week_range = current_week_range.split('_')
                start_month, start_day = current_week_range[0].split('-')[1:]
                end_month, end_day = current_week_range[1].split('-')[1:]
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.start_current_day.text = start_day
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.end_current_day.text = end_day
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.start_current_month.text = NumStr2Month[start_month]
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.end_current_month.text = NumStr2Month[end_month]
        else:
            if MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.start_current_day.text != '':
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.start_current_day.text = ''
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.end_current_day.text = ''
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.start_current_month.text = ''
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.end_current_month.text = ''
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.current_week = ''

    def update_current_week(self, *args):
        calendar_full = MDApp.get_running_app().calendar_full
        cycle = MDApp.get_running_app().cycle
        # update current day
        MDApp.get_running_app().current_day = datetime.datetime.now().strftime('%a')
        if MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.current_day != MDApp.get_running_app().current_day and calendar_full is not None and MDApp.get_running_app().current_week_range is not None:
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = 'none_filter'
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.current_day = MDApp.get_running_app().current_day
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.change_day()

        if calendar_full is not None and calendar_full != {}:
            # update calendar display in calendar page
            date_now = datetime.datetime.now().strftime('%Y-%m-%d')
            for week_range in calendar_full:
                week_start, week_end = week_range.split('_')[:2]
                if week_start <= date_now <= week_end:
                    if week_range != MDApp.get_running_app().current_week_range:
                        MDApp.get_running_app().current_week_range = week_range
                        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
                    break
    def update_alarm(self,*args):
        if MDApp.get_running_app().calendar_full is not None and MDApp.get_running_app().calendar_full != {}:
            calendar_full = MDApp.get_running_app().calendar_full
            date_now = datetime.datetime.now().strftime('%Y-%m-%d')
            day_now = datetime.datetime.now().strftime('%A').lower()

            for week_range in calendar_full:
                week_start, week_end = week_range.split('_')[:2]
                if week_start <= date_now <= week_end:
                    if MDApp.get_running_app().now in calendar_full[week_range][day_now]:
                        if MDApp.get_running_app().alarm_ringtone.state != 'play':
                            MDApp.get_running_app().alarm_ringtone.play()
                    else:
                        if MDApp.get_running_app().alarm_ringtone.state == 'play':
                            MDApp.get_running_app().alarm_ringtone.stop()
                    break
    def update_calendar_list(self):
        filter = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content
        if filter != 'none_filter':
            calendar_full = filter_calendar_full_by_plantid(MDApp.get_running_app().calendar_full, filter)
        else:
            calendar_full = MDApp.get_running_app().calendar_full

        # update calendar display in calendar page
        # clear widget
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.reset_calendar()
        if calendar_full == {}:
            return
        MDApp.get_running_app().current_week_range = get_current_week_range()
        current_calendar_full = calendar_full[MDApp.get_running_app().current_week_range]

        # put calendar in to display
        for day, hours in current_calendar_full.items():
            for hour, task_list in hours.items():
                current_closest = find_closest_number(hour)
                if len(task_list) == 0:
                    continue
                task_widget = GridLayout(cols=len(task_list), pos_hint = {'center_x':0.5}, spacing = '1dp')
                for task in task_list:
                    a = Image(pos_hint={'center_y': 0.5}, source='', color=task['represent_color'])
                    task_widget.add_widget(a)

                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.week.ids[day].ids[
                    current_closest].ids.hour_box.add_widget(task_widget)
    def change_day(self,instance = None, day = None):
        if instance is None:
            if day is None:
                instance = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids[MDApp.get_running_app().current_day]
            else:
                instance = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids[day]

        # set plant filter
        filter = MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content
        if filter != 'none_filter':
            calendar_full = filter_calendar_full_by_plantid(MDApp.get_running_app().calendar_full, filter)
        else:
            calendar_full = MDApp.get_running_app().calendar_full
        day_list = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        for day in day_list:
            self.ids[day].background_color = (0,0,0,0)
        instance.background_color = list(MDApp.get_running_app().background_color[:3])+[0.5]

        self.ids.task_display.clear_widgets()

        if calendar_full == {}:
            a = EmptyTaskWidget()
            self.ids.task_display.add_widget(a)
            return

        # filter the selected day column of calendar
        # this calendar have every task from week 1, which can be unavailable in current week
        first_week_range = next(iter(calendar_full))
        primal_calendar_full = calendar_full[first_week_range][Day2Day[instance.name]]
        # this calendar is from current week
        current_week_index = list(calendar_full.keys()).index(MDApp.get_running_app().current_week_range)
        calendar_full = calendar_full[MDApp.get_running_app().current_week_range][Day2Day[instance.name]]
        hour_boxs = {'4':[],'8':[],'12':[],'16':[],'20':[],'0':[]}
        for hour, tasks in primal_calendar_full.items():
            hour_boxs[find_closest_number(hour)].append({hour:tasks})
        for hour_box, hours_tasks in hour_boxs.items():
            if hours_tasks != []:
                for hour_task in hours_tasks:
                    if list(hour_task.values())[0] != []:
                        a = HourBoxWidget()
                        a.ids.empty_calendar.text = '• ' + HourBox2Text[hour_box]
                        self.ids.task_display.add_widget(a)
                        break
                for hour_task in hours_tasks:
                    if hour_task != {}:
                        for hour, tasks in hour_task.items():
                            for task in tasks:
                                b = TaskWidget()
                                setattr(b, 'name', task['name'])
                                setattr(b,'hour',hour)
                                setattr(b, 'represent_color', task['represent_color'])
                                setattr(b, 'task', task['task'])
                                if hour not in calendar_full or task not in calendar_full[hour]:
                                    setattr(b, 'text_color', (0.5,0.5,0.5,0.5))
                                    try:
                                        remaining_week = str(int(task['frequency'])-(current_week_index % int(task['frequency'])))
                                        remaining_week = 'available in '+remaining_week+' week'+('s' if remaining_week != '1' else '')
                                        setattr(b, 'status', remaining_week)
                                    except:
                                        setattr(b, 'status', 'unavailable this week')
                                self.ids.task_display.add_widget(b)

    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'change_calendar':
            change_size = Animation(height = instance.height*0.95, width = instance.width*0.95, disabled=True,
                                    center_x=instance.center_x, center_y=instance.center_y, duration=0.01,
                                    background_color = MDApp.get_running_app().press_word_button)
            change_size.start(self.ids.change_calendar)
        else:
            change_size.start(self.ids.filter_button_image)
    def release_button(self,instance):
        change_size = Animation(width=instance.width, height=instance.height, disabled=False,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'change_calendar':
            change_size = Animation(size_hint=(0.5, 0.75), disabled=False,
                                    center_x=instance.center_x, center_y=instance.center_y, duration=0.01,
                                    background_color = MDApp.get_running_app().secondary_background_color)
            change_size.start(self.ids.change_calendar)
        else:
            change_size.start(self.ids.filter_button_image)

    def load_filter_selector(self,instance):
        Factory.PickCalendarFilterPopup().open()
    def edit_calendar(self):
        if self.ids.filter_button.content == 'none_filter':
            Factory.PickCalendarFilterForEditPopup().open()
        else:
            Factory.ConfirmEditCalendarPopup().open()



class CommunityPage(Screen):
    pass
class SearchResult(ThreeLineIconListItem):
    def open_search_item(self,instance):
        # disable the buttons
        self.parent.parent.parent.parent.parent.ids.filter_button.disabled = True
        self.parent.parent.parent.parent.parent.ids.search_bar.disabled = True
        self.parent.parent.parent.parent.parent.ids.search_button.disabled = True

        # update information to wiki_page class
        self.parent.parent.parent.parent.parent.item_url = instance.url
        info, descryption = SearchItem(instance.url)
        self.parent.parent.parent.parent.parent.item_info = info
        self.parent.parent.parent.parent.parent.item_descryption = descryption

        # change screen
        self.parent.parent.parent.parent.transition = CardTransition()
        self.parent.parent.parent.parent.transition.mode = 'push'
        self.parent.parent.parent.parent.transition.duration = 0.5
        self.parent.parent.parent.parent.transition.direction = 'left'
        self.parent.parent.parent.parent.current = 'encyclopedia_search_item'

class SearchItemScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.scroll_view.scroll_y = 1
        self.ids.info.text = self.parent.parent.item_info
        self.ids.descryption.text = self.parent.parent.item_descryption
    def press_back(self, instance):  # Back button
        animate = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)

    def release_back(self, instance):
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.back_button_image)
        # re-enable the button
        self.parent.parent.ids.filter_button.disabled = False
        self.parent.parent.ids.search_bar.disabled = False
        self.parent.parent.ids.search_button.disabled = False

        # change screen
        self.parent.transition.mode = 'pop'
        self.parent.transition.duration = 0.5
        self.parent.transition.direction = 'right'
        self.parent.current = 'encyclopedia_search_screen'
class FilterScreen(Screen):
    def change_filter(self,instance):
        self.ids.none_filter.background_color = (0,0,0,0)
        self.ids.comname_filter.background_color = (0, 0, 0, 0)
        self.ids.sciname_filter.background_color = (0, 0, 0, 0)
        instance.background_color = MDApp.get_running_app().secondary_background_color
    def shut_selector(self,instance):
        self.parent.parent.parent.parent.ids.filter_button.content = instance.content
        self.parent.transition.direction = 'up'
        self.parent.transition.duration = 0.2
        self.parent.current = 'filter_null'
class WikiPage(Screen):
    first_page_url = ''
    previous_page_url = ''
    next_page_url = ''
    last_page_url = ''
    item_url = ''
    item_info = ''
    item_descryption = ''

    def start_crawling(self,direction=''):
        self.ids.scroll_view.scroll_y = 1
        self.ids.first_page.allowed = False
        self.ids.previous_page.allowed = False
        self.ids.next_page.allowed = False
        self.ids.last_page.allowed = False

        self.ids.curr_over_total.text=''
        if self.ids.search_bar.text == '':
            return
        self.ids.search_list.clear_widgets()

        if direction == 'first':
            url = self.first_page_url
        elif direction == 'previous':
            url = self.previous_page_url
        elif direction=='next':
            url = self.next_page_url
        elif direction=='last':
            url = self.last_page_url
        else:
            content = '%20'.join(self.ids.search_bar.text.strip().split())
            url = 'https://www.botanyvn.com/cnt.asp?param=edir&q='+content+'&t='+self.ids.filter_button.content

        item_list,page_list =SearchDisplay(url)
        if item_list == []:
            display_item = SearchResult(id = 'not_found',
                                        text='No search result found!',
                                        secondary_text='-',
                                        tertiary_text='pleade try again with another keyword',
                                        disabled = True)
            #print(display_item.ids)
            self.ids.search_list.add_widget(display_item)
            return

        # Get total page count and current page number
        total_page = len(page_list)+1
        curr_page = 1
        if '&pg=' in url:
            curr_page = int(url.split('&pg=')[1])

        if total_page ==1:
            self.first_page_url=''
            self.ids.first_page.allowed = False
            self.previous_page_url=''
            self.ids.previous_page.allowed = False
            self.next_page_url=''
            self.ids.next_page.allowed = False
            self.last_page_url=''
            self.ids.last_page.allowed = False
        elif curr_page == 1 and total_page != curr_page:
            self.first_page_url = ''
            self.ids.first_page.allowed = False
            self.previous_page_url = ''
            self.ids.previous_page.allowed = False
            self.next_page_url = url.split('&pg=')[0]+'&pg='+str(curr_page+1)
            self.ids.next_page.allowed = True
            self.last_page_url = url.split('&pg=')[0]+'&pg='+str(total_page)
            self.ids.last_page.allowed = True
        elif total_page == curr_page:
            self.first_page_url = url.split('&pg=')[0]+'&pg=1'
            self.ids.first_page.allowed = True
            self.previous_page_url = url.split('&pg=')[0]+'&pg='+str(curr_page-1)
            self.ids.previous_page.allowed = True
            self.next_page_url = ''
            self.ids.next_page.allowed = False
            self.last_page_url = ''
            self.ids.last_page.allowed = False
        else:
            self.first_page_url = url.split('&pg=')[0] + '&pg=1'
            self.ids.first_page.allowed = True
            self.previous_page_url = url.split('&pg=')[0] + '&pg=' + str(curr_page - 1)
            self.ids.previous_page.allowed = True
            self.next_page_url = url.split('&pg=')[0] + '&pg=' + str(curr_page + 1)
            self.ids.next_page.allowed = True
            self.last_page_url = url.split('&pg=')[0] + '&pg=' + str(total_page)
            self.ids.last_page.allowed = True

        self.ids.curr_over_total.text = str(curr_page)+'/'+str(total_page)
        for item in item_list:
            display_item = SearchResult(id='_'.join(item['name'].split()),
                                        text=item['name'],
                                        secondary_text=item['type'],
                                        tertiary_text=item['info'],
                                        disabled = False)
            setattr(display_item,'url',item['url'])
            display_item.height = self.height / 10
            self.ids.search_list.add_widget(display_item)

    def load_filter_selector(self,instance):
        self.ids.filter_selector_manager.transition = SlideTransition()
        self.ids.filter_selector_manager.transition.duration = 0.2
        if self.ids.filter_selector_manager.current == 'filter_null':
            self.ids.filter_selector_manager.transition.direction = 'down'
            self.ids.filter_selector_manager.current = 'filter_select'
        else:
            self.ids.filter_selector_manager.transition.direction = 'up'
            self.ids.filter_selector_manager.current = 'filter_null'
    def press_button(self,instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled = True,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'filter_button':
            change_size.start(self.ids.filter_button_image)
        else:
            change_size.start(self.ids.search_button_image)
    def release_button(self,instance):
        change_size = Animation(width=instance.width, height=instance.height, disabled = False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'filter_button':
            change_size.start(self.ids.filter_button_image)
        else:
            change_size.start(self.ids.search_button_image)

    pass
class PurchaseWaitingPopUP(Popup):
    pass
class ShoppingPage(Screen):
    def press_button(self, instance):
        instance.disabled = True
        self.ids[instance.name.split('_button')[0] + '_background'].color = MDApp.get_running_app().press_word_button

    def release_button(self, instance):
        instance.disabled = False
        self.ids[instance.name.split('_button')[0]+'_background'].color = MDApp.get_running_app().background_color
    def purchase(self, energy = 0, seed = 0, subscription_status = '', price = ''):
        self.popup = Factory.PurchaseWaitingPopUP()
        self.popup.open()
        Clock.schedule_once(partial(self.purchase_, energy, seed, subscription_status, price), 1)

    def purchase_(self, energy,seed,subscription_status,price,dt):
        energy = energy*100
        seed = seed
        response = press_paypal_button(username=MDApp.get_running_app().current_username,
                                       energy=energy, seed=seed, subscription_status=subscription_status,
                                       amount=price)
        if response:
            MDApp.get_running_app().root.ids.master_screen.recalculate(energy= energy, seed=seed,subscription_status=subscription_status)
            MDApp.get_running_app().play_sound('success.wav')
            self.popup.dismiss()
        else:
            self.popup.dismiss()
            MDApp.get_running_app().play_sound('unsuccess.wav')
            Factory.FailConfirmPopup(title = 'Purchase unsuccessful. Please check connection and try again').open()


class MainPagesManager(ScreenManager):
    pass
class UtilityBars(FloatLayout):
    def home_buttons_animation(self, instance): # animation for home buttons
        if HomeButtons2Num[instance.name] != self.parent.parent.parent.Previous_home_buttons:
            animate = Animation(pos_hint=instance.pos_hint, duration=0.1)
            animate.start(self.ids.home_highlight)
            self.parent.parent.parent.ids.main_pages.transition = SlideTransition()
            self.parent.parent.parent.ids.main_pages.transition.duration = 0.2
            # move left/right depend on previous button position
            if HomeButtons2Num[instance.name] > self.parent.parent.parent.Previous_home_buttons:
                self.parent.parent.parent.ids.main_pages.transition.direction = 'left'
            else:
                self.parent.parent.parent.ids.main_pages.transition.direction = 'right'
            # Change screen when press those buttons
            self.parent.parent.parent.ids.main_pages.current = instance.name+'_page'
            self.parent.parent.parent.Previous_home_buttons = HomeButtons2Num[instance.name]
class LogoutPopup(Popup):
    def press_button(self, instance):
        instance.disabled = True
        instance.color = MDApp.get_running_app().press_word_button
    def release_button(self, instance):
        instance.disabled = False
        if instance.text == 'logout':
            instance.color = MDApp.get_running_app().wrong_pass_warn
        else:
            instance.color = MDApp.get_running_app().primary_font_color
    def logout(self, instance):
        MDApp.get_running_app().root.ids.master_screen.logout()
        self.dismiss()
class SettingScreen(Screen):
    def press_button(self, instance):
        change_size = Animation(width=instance.width * 0.95, height=instance.height * 0.95, disabled=True,
                                center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        if instance.name == 'logout_button':
            change_size.start(self.ids.logout_button)

    def release_button(self, instance):
        if instance.name == 'logout_button':
            change_size = Animation(size_hint=(0.8, 0.5), disabled=False,
                                    center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
            change_size.start(self.ids.logout_button)
    def donate_us(self,source = 'momo'):
        donate_us(source = source)
class MasterScreen(Screen):
    Previous_home_buttons = 0
    current_filter_screen = ''
    def on_pre_enter(self, *args):
        # update time at load
        Clock.schedule_interval(self.ids.main_pages.ids.home_page.update_time, 1)
        Clock.schedule_interval(self.ids.main_pages.ids.home_page.get_next_event, 1)
        Clock.schedule_interval(self.ids.main_pages.ids.calendar_page.update_cycle, 1)
        Clock.schedule_interval(self.ids.main_pages.ids.calendar_page.update_alarm, 1)
        Clock.schedule_interval(self.ids.main_pages.ids.calendar_page.update_current_week, 1)

        # update login status
        WriteHadLogin()

        # update user
        MDApp.get_running_app().current_username, MDApp.get_running_app().subscription_status, MDApp.get_running_app().energy, MDApp.get_running_app().seed = update_current_user(MDApp.get_running_app().current_user)
        MDApp.get_running_app().cycle = get_cycle()
        MDApp.get_running_app().calendar_full = get_calendar_full()
        # update item count
        self.ids.energy_count.text = str(round(MDApp.get_running_app().energy,2))
        self.ids.seed_count.text = str(MDApp.get_running_app().seed)
        # update current plant list
        MDApp.get_running_app().plant_list = get_plant_list()
        MDApp.get_running_app().plant_list_advanced = get_plant_list_advanced()
        MDApp.get_running_app().plant_calendar = get_plant_calendar()
        MDApp.get_running_app().plant_conversation = get_plant_conversation()
        MDApp.get_running_app().current_week_range = get_current_week_range()
        # update screen that contain the list
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.update_plant_list()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.current_plant = ''
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.current_plant_chat = ''

        if MDApp.get_running_app().subscription_status == 'free':
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.pro_feature_chat.opacity = 1
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_background.color = MDApp.get_running_app().background_color
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_button.disabled = False
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_checkmark.opacity = 0
        else:
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.pro_feature_chat.opacity = 0
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_background.color = MDApp.get_running_app().secondary_background_color
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_button.disabled = True
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_checkmark.opacity = 0.5
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.update_calendar_list()
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.ids.filter_button.content = 'none_filter'
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.calendar_page.current_day = ''

        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.mode = 'normal'
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_box_scrollview.scroll_y = 1
        MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.profile_display_chatbox_scrollview.scroll_y = 1

        #update current screen
        self.ids.utility_bars.ids.home_highlight.pos_hint = self.ids.utility_bars.ids.home.pos_hint
        self.Previous_home_buttons = 0
        self.ids.main_and_setting.current = 'normal_master_screen'
        self.ids.main_pages.current = 'home_page'
    def open_setting(self, instance):
        if self.ids.main_and_setting.current == 'normal_master_screen':
            self.ids.main_and_setting.transition = CardTransition()
            self.ids.main_and_setting.transition.mode = 'push'
            self.ids.main_and_setting.transition.duration = 0.25
            self.ids.main_and_setting.transition.direction = 'down'
            self.ids.main_and_setting.current = 'setting_screen'
        else:
            self.ids.main_and_setting.transition = CardTransition()
            self.ids.main_and_setting.transition.mode = 'pop'
            self.ids.main_and_setting.transition.duration = 0.25
            self.ids.main_and_setting.transition.direction = 'up'
            self.ids.main_and_setting.current = 'normal_master_screen'
    def swipe_home_buttons(self, instance):
        print('swipe')
    def logout(self):
        WriteHadLogin(False)
        self.parent.transition = FadeTransition()
        self.parent.current = 'login_screen'
    def recalculate(self,energy = 0, seed = 0, subscription_status = ''):
        change_energy = False
        change_seed = False
        change_subscription_status = False
        if energy != 0:
            MDApp.get_running_app().energy += energy / 100
            MDApp.get_running_app().root.ids.master_screen.ids.energy_count.text = str(
                round(MDApp.get_running_app().energy, 2))
            MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.plant_chat_screen.ids.energy_count.text = MDApp.get_running_app().root.ids.master_screen.ids.energy_count.text
            change_energy = True
        if seed != 0:
            MDApp.get_running_app().seed += seed
            MDApp.get_running_app().root.ids.master_screen.ids.seed_count.text = str(MDApp.get_running_app().seed)
            change_seed = True
        if subscription_status != '':
            if subscription_status == 'free':
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.pro_feature_chat.opacity = 1
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_background.color = MDApp.get_running_app().background_color
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_button.disabled = False
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_checkmark.opacity = 0
            else:
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.plant_profile_page.ids.pro_feature_chat.opacity = 0
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_background.color = MDApp.get_running_app().secondary_background_color
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_button.disabled = True
                MDApp.get_running_app().root.ids.master_screen.ids.main_pages.ids.shopping_page.ids.pro_tier_checkmark.opacity = 0.5
            MDApp.get_running_app().subscription_status = subscription_status
            change_subscription_status = True

        if True in [change_energy, change_seed, change_subscription_status]:
            save_recalculate(id=MDApp.get_running_app().current_user,
                             change_energy=change_energy,
                             energy=MDApp.get_running_app().energy,
                             change_seed=change_seed,
                             seed=MDApp.get_running_app().seed,
                             change_subscription_status=change_subscription_status,
                             subscription_status=MDApp.get_running_app().subscription_status)

class StartUp(Screen):
    def on_kv_post(self, *args):
        animate = Animation(duration=1)+Animation(color = (1,1,1,1),duration=2)+Animation(duration=2)
        animate.start(self.ids.logo)
        animate.bind(on_complete = self.to_next)

    def to_next(self, *args):
        self.parent.transition = FadeTransition()
        if ReadHadLogin():
            self.parent.current = 'master_screen'
        elif ReadHadStartup():
            self.parent.current = 'login_screen'
        else:
            self.parent.current = 'sign_up_screen'
class LoginScreen(Screen):
    def on_pre_enter(self, *args):
        # reset these fields
        self.ids.username.text = ''
        self.ids.password.text = ''
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
        isUser = [False, None]
        if isUsernameFormat(self.ids.username.text) and isUsernameFormat(self.ids.password.text):
            isUser = simple_login_validation(self.ids.username.text.lower(),self.ids.password.text)

        animate = Animation(width=instance.width, height=instance.height, disabled = False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.login_button_image)
        self.ids.login_button_image.source = 'layout/img/login.png'

        if isUser[0]: # Validated
            # set startup status
            WriteHadStartUp()
            MDApp.get_running_app().current_user = isUser[1]
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
            # change screen
            #self.parent.transition.duration = 0.5
            #self.parent.transition.direction = 'left'
            #self.parent.current = 'forget_password_email_screen'
            pass

        # Sign up-------------------------------------------
        else:
            change_size.start(self.ids.sign_up_image)
            change_color += Animation(color=MDApp.get_running_app().primary_font_color, duration=0.1)
            change_color.start(instance)
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'right'
            self.parent.current = 'sign_up_screen'
class ForgetPasswordEmailScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.email_forget.text = ''
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
            MDApp.get_running_app().otp = get_otp(self.ids.email_forget.text)
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
    def on_pre_enter(self, *args):
        self.ids.otp_pass1.text = ''
        self.ids.otp_pass2.text = ''
        self.ids.otp_pass3.text = ''
        self.ids.otp_pass4.text = ''
        self.ids.otp_pass5.text = ''
        self.ids.otp_pass6.text = ''
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
        isOTP = simple_otp_validation(MDApp.get_running_app().otp, otp)
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
        MDApp.get_running_app().otp = get_otp(self.parent.ids.forget_password_email_screen.ids.email_forget.text)
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
    def on_pre_enter(self, *args):
        # reset all these fields
        self.ids.new_password.text = ''
        self.ids.new_password2.text = ''
    def press_confirm_animation(self,instance): # Shrink button
        animate = Animation(width=instance.width*0.95, height= instance.height*0.95, disabled = True,
                            center_x = instance.center_x, center_y = instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_new_pass_button_image)
        self.ids.confirm_new_pass_button_image.source = 'layout/img/login_pressed.png'
    def login(self,instance): # Expand button and validate
        email = self.parent.ids.forget_password_email_screen.ids.email_forget.text
        isNew = [False, None]
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
        if isNew[0]:
            # set startup status
            WriteHadStartUp()
            MDApp.get_running_app().current_user = isNew[1]
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'up'
            self.parent.current = 'master_screen'
        else:
            animate = Animation(color = MDApp.get_running_app().wrong_pass_warn,
                                duration=0.2)+Animation(duration=2)+Animation(color = (0,0,0,0),duration=0.5)
            animate.start(self.ids.wrong)
class SignUpScreen(Screen):
    def on_pre_enter(self, *args):
        # reset all these fields
        self.ids.username_sign_up.text = ''
        self.ids.email_sign_up.text = ''
        self.ids.password_sign_up.text = ''
        self.ids.password_sign_up2.text = ''
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
            self.ids.wrong.text = 'Username is insufficient'
        elif not isUsernameFormat(self.ids.email_sign_up.text):
            self.ids.wrong.text = 'Email is insufficient'
        elif not isPasswordFormat(self.ids.password_sign_up.text):
            self.ids.wrong.text = 'Password must be at least 8 characters,\n contain numbers and capital letters'
        else:
            message, isNewUser = simple_new_user_validation(self.ids.username_sign_up.text,self.ids.email_sign_up.text)
            if not isNewUser:
                self.ids.wrong.text = message

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
            MDApp.get_running_app().otp = get_otp(self.ids.email_sign_up.text)
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
            # change screen
            self.parent.transition.duration = 0.5
            self.parent.transition.direction = 'left'
            self.parent.current = 'login_screen'
class SignUpOTPScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.otp_pass1.text = ''
        self.ids.otp_pass2.text = ''
        self.ids.otp_pass3.text = ''
        self.ids.otp_pass4.text = ''
        self.ids.otp_pass5.text = ''
        self.ids.otp_pass6.text = ''
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
        isOTP = simple_otp_validation(MDApp.get_running_app().otp, otp)
        animate = Animation(width=instance.width, height=instance.height, disabled=False,
                            center_x=instance.center_x, center_y=instance.center_y, duration=0.01)
        animate.start(self.ids.confirm_otp_button_image)
        self.ids.confirm_otp_button_image.source = 'layout/img/login.png'
        if isOTP:
            signup_status, new_user = simple_signup_vadilation(self.parent.ids.sign_up_screen.ids.username_sign_up.text,
                                     self.parent.ids.sign_up_screen.ids.email_sign_up.text,
                                     self.parent.ids.sign_up_screen.ids.password_sign_up.text)
            if signup_status:
                # set startup status
                WriteHadStartUp()
                # update
                update_plant_after_signup(new_user)
                MDApp.get_running_app().current_user = new_user
                # change screen
                self.parent.transition.duration = 0.5
                self.parent.transition.direction = 'up'
                self.parent.current = 'master_screen'
            else:
                # Validation failed
                self.ids.wrong_otp.text = 'failed to validate'
                animate = Animation(color=MDApp.get_running_app().wrong_pass_warn,
                                    duration=0.2) + Animation(duration=1) + Animation(color=(0, 0, 0, 0), duration=0.5)
                animate.start(self.ids.wrong_otp)
        else:
            # Validation failed
            self.ids.wrong_otp.text = 'wrong otp'
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
        MDApp.get_running_app().otp = get_otp(self.parent.ids.sign_up_screen.ids.email_sign_up.text)
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
    theme_list = theme_list
    alarm_ringtone = SoundLoader.load(alarm_ringtone)
    background_image = background_image

    current_user = current_user
    current_username = None
    subscription_status = None
    energy = None
    seed = None

    plant_list = None
    plant_list_advanced = None
    plant_calendar = None
    plant_conversation = None

    cycle = None
    calendar_full = None

    current_week_range = None
    current_day = None

    otp = None

    icon = get_file_path('layout/img/logo.png')
    @property
    def primary_font_color(self):
        return self.theme_list[self.theme]['primary_font_color']
    @property
    def secondary_font_color(self):
        return self.theme_list[self.theme]['secondary_font_color']
    @property
    def background_color(self):
        return self.theme_list[self.theme]['background_color']
    @property
    def primary_background_color(self):
        return self.theme_list[self.theme]['primary_background_color']
    @property
    def secondary_background_color(self):
        return self.theme_list[self.theme]['secondary_background_color']
    @property
    def wrong_pass_warn(self):
        return self.theme_list[self.theme]['wrong_pass_warn']
    @property
    def press_word_button(self):
        return self.theme_list[self.theme]['press_word_button']
    @property
    def highlight_button(self):
        return self.theme_list[self.theme]['highlight_button']
    @property
    def dark_grey(self):
        return self.theme_list[self.theme]['dark_grey']
    def play_sound(self, filename):
        #sound = SoundLoader.load(self.get_file_path('soundfx/'+filename))
        #if sound:
            #sound.volume = self.volume
            #sound.play()
        pass

    def build(self):
        self.now = datetime.datetime.now().strftime('%H:%M')
        self.today = datetime.datetime.today().strftime('%A, %d %B')
        kv = Builder.load_file('layout/MainLayout.kv')
        return kv
    def get_file_path(self,file: str):
        return file

if __name__ == '__main__':
    PlantApp().run()
