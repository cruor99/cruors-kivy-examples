from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from permissions.location import check_permission, ask_permission

class ExampleRoot(BoxLayout):

    def check_fine_location_permission(self):
        check_permission("android.permission.ACCESS_FINE_LOCATION")

    def request_fine_location_permission(self):
        ask_permission("android.permission.ACCESS_FINE_LOCATION")




class ExampleApp(App):
    def build(self):
        return ExampleRoot()

if __name__ == '__main__':
    ExampleApp().run()