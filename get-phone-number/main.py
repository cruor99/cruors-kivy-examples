from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.logger import Logger

from jnius import PythonJavaClass, java_method, autoclass
from permissions.location import check_permission, ask_permission

PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity
Context = autoclass('android.content.Context')


class NumberRoot(BoxLayout):
    def grab_number(self):
        if check_permission("android.permission.READ_PHONE_STATE"):
            Logger.info("Has correct permission")
            telephone_manager = PythonActivity.getSystemService(Context.TELEPHONY_SERVICE)
            phone_number = telephone_manager.getLine1Number()
            Logger.info(phone_number)
            self.ids.phone_number.text = phone_number
        else:
            Logger.info("Requesting permission")
            ask_permission("android.permission.READ_PHONE_STATE")

class NumberApp(App):

    def build(self):
        return NumberRoot()

if __name__ == "__main__":
    NumberApp().run()