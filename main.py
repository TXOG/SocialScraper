import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

kivy.require("1.11.1")


class Page1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        label = Label(text="Social Scraper", font_size=40, halign="center", valign="middle")
        layout.add_widget(label)
        button = Button(text="Discord", font_size=16, on_release=self.go_to_page2)
        layout.add_widget(button)
        self.add_widget(layout)

    def go_to_page2(self, instance):
        self.manager.current = "page2"


class Page2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        label = Label(text="Enter discord user's ID:", font_size=24)
        layout.add_widget(label)
        self.input = TextInput(font_size=24)
        layout.add_widget(self.input)
        button = Button(text="Lookup", font_size=24, on_release=self.lookup)
        layout.add_widget(button)
        self.add_widget(layout)

    def lookup(self, instance):
        user_id = self.input.text
        print("The user entered:", user_id)


class SocialScraperApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Page1(name="page1"))
        sm.add_widget(Page2(name="page2"))
        return sm


if __name__ == "__main__":
    SocialScraperApp().run()
