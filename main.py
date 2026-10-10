import sys
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

IS_ANDROID = sys.platform == 'android'

if IS_ANDROID:
    from jnius import autoclass
    Settings = autoclass('android.provider.Settings')
    Intent = autoclass('android.content.Intent')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

CONFIG_FILE = "device_config.json"

class KidWatchApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with self.layout.canvas.before:
            Color(*get_color_from_hex('#111827'))
            self.bg_rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_bg, pos=self._update_bg)

        self.device_key = self.load_device_key()

        if self.device_key:
            self.show_active_screen()
            if IS_ANDROID:
                self.start_background_service()
        else:
            self.show_login_screen()

        return self.layout

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def show_login_screen(self):
        self.layout.clear_widgets()
        
        self.layout.add_widget(Label(
            text="[b]KidWatch[/b] Protection",
            markup=True,
            font_size='24sp',
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height='40dp'
        ))
        
        self.layout.add_widget(Label(
            text="ওয়েবসাইট থেকে পাওয়া Device Key টি নিচে লিখুন:",
            font_size='14sp',
            color=(0.8, 0.8, 0.8, 1)
        ))
        
        self.key_input = TextInput(
            hint_text="e.g. 8f9b2c3d-xxxx...",
            multiline=False,
            size_hint_y=None,
            height='45dp'
        )
        self.layout.add_widget(self.key_input)

        save_btn = Button(
            text="Save & Connect Device",
            size_hint_y=None,
            height='50dp',
            background_normal='',
            background_color=get_color_from_hex('#2563EB')
        )
        save_btn.bind(on_release=self.save_and_activate)
        self.layout.add_widget(save_btn)

    def show_active_screen(self):
        self.layout.clear_widgets()
        
        self.layout.add_widget(Label(
            text="● Service Status: [color=00FF88]ACTIVE[/color]",
            markup=True,
            font_size='20sp',
            bold=True
        ))
        
        self.layout.add_widget(Label(
            text=f"Linked Key: {self.device_key[:8]}...",
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1)
        ))

        perm_btn = Button(
            text="Enable Notification Permission",
            size_hint_y=None,
            height='50dp',
            background_normal='',
            background_color=get_color_from_hex('#059669')
        )
        perm_btn.bind(on_release=self.open_notification_settings)
        self.layout.add_widget(perm_btn)

    def save_and_activate(self, instance):
        input_key = self.key_input.text.strip()
        if input_key:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"device_key": input_key}, f)
            self.device_key = input_key
            self.show_active_screen()
            if IS_ANDROID:
                self.start_background_service()

    def load_device_key(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f).get("device_key")
            except Exception:
                return None
        return None

    def start_background_service(self):
        try:
            mActivity = PythonActivity.mActivity
            service_class = autoclass('org.kidwatch.ServiceKidservice')
            service_class.start(mActivity, '')
            print("Service started successfully!")
        except Exception as e:
            print("Failed to start service:", e)

    def open_notification_settings(self, instance=None):
        if IS_ANDROID:
            try:
                activity = PythonActivity.mActivity
                intent = Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)
                activity.startActivity(intent)
            except Exception as e:
                print("Could not open settings:", e)

if __name__ == '__main__':
    KidWatchApp().run()