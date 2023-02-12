# Kivy imports
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager

# DCF + imports
import requests
import webbrowser
from selenium import webdriver
import time
import json
from selenium.webdriver.chrome.options import Options

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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        begining_of_url = "https://lookup.guru/"
        target_id = self.input.text
        whole_url = begining_of_url + str(target_id)
        driver.get(whole_url)
        time.sleep(5)
        images = driver.find_elements_by_tag_name('img')
        for image in images:
            global pfp
            pfp = (image.get_attribute('src'))
            break
        img_data = requests.get(pfp).content
        with open('pfpimage.png', 'wb') as handler:
            handler.write(img_data)
        filePath = "pfpimage.png"
        searchUrl = 'https://yandex.com/images/search'
        files = {'upfile': ('blob', open(filePath, 'rb'), 'image/jpeg')}
        params = {'rpt': 'imageview', 'format': 'json',
                  'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
        response = requests.post(searchUrl, params=params, files=files)
        query_string = json.loads(response.content)['blocks'][0]['params']['url']
        img_search_url = searchUrl + '?' + query_string
        webbrowser.open(img_search_url)

class SocialScraperApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Page1(name="page1"))
        sm.add_widget(Page2(name="page2"))
        return sm


if __name__ == "__main__":
    SocialScraperApp().run()
