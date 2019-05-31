from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

class ExampleRoot(BoxLayout):
    counter = NumericProperty(0)

    def toggle_main_button_disable(self):
        if self.ids.main_button.disabled == True:
            self.ids.main_button.disabled = False
        else:
            self.ids.main_button.disabled = True


class ExampleApp(App):

    def build(self):
        return ExampleRoot()


if __name__ == "__main__":
    ExampleApp().run()