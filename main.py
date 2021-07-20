# imports
import pyperclip
import requests
import datetime
from io import BytesIO
import win32clipboard
from PIL import Image
from pynput import keyboard

# variables
keybind = {keyboard.Key.shift, keyboard.Key.cmd, keyboard.KeyCode.from_char('C')}
theme = "panda"
language = "auto"
path = "C:/Users/Tom/OneDrive/Documents/Illustrator/PNG/carbon"

# main class
class Keyboard_listener():
    def __init__(self, keys):
        self.combination = keys
        self.currently_pressed = set()
        self.is_pressed = False

        listener = keyboard.Listener(on_press=self._on_press)
        listener.start()

    def _on_press(self, key):
        if key in self.combination:
            self.currently_pressed.add(key)

        if self.currently_pressed == self.combination:
            self.is_pressed = True
            Clipboard_to_image(theme, language, path).get_clipboard_text()

class Clipboard_to_image():
    def __init__(self, theme, language, path):
        self.theme = theme
        self.language = language
        self.path = path

    def add_clipboard(self, name):
        print("clipboard")
        # grabbing image from path of image
        image = Image.open(f"{self.path}{str(name)}.png")
    
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()  
        
        # copying image to clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)    
        win32clipboard.CloseClipboard()

    def get_clipboard_text(self):
        # get clipboard text
        print("text")
        self.send_request(pyperclip.paste())
    
    def send_request(self, text):
        print("request")
        # making requests
        url_carbonara = "https://carbonara.vercel.app/api/cook"
        headers = {"Content-Type": "application/json"}
        # making name of file
        data = {"code":f"{text}",  "backgroundColor": "#1F816D"}
        # editing name to make file savable
        name = str(datetime.datetime.now())
        name = name.replace(".","-")
        name = name.replace(" ","_")
        name = name.replace(":","-")
        # sending request
        resp = requests.post(url_carbonara, headers=headers, json=data)

        # saving file
        open(f"{self.path}{str(name)}.png", 'wb').write(resp.content)
        self.add_clipboard(name)

if __name__ == '__main__':
    text_to_image = Clipboard_to_image(theme, language, path)
    key_listener = Keyboard_listener(keybind)
    input()