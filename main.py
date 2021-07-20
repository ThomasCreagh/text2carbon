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

# This class listens to your keyboard and checks if you press the keybind
class Keyboard_listener():
    # Sets vabibles needed for the keyboard listener
    def __init__(self, keys):
        self.combination = keys
        self.currently_pressed = set()
        self.is_pressed = False

        # Starts the listener
        listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        listener.start()

    # This will run when a key is pressed
    def _on_press(self, key):
        if key in self.combination:
            self.currently_pressed.add(key)

        if self.currently_pressed == self.combination:
            self.is_pressed = True
    
    # This will run when a key or keybind is released
    def _on_release(self, key):
        try:
            self.currently_pressed.remove(key)

            if self.is_pressed and len(self.currently_pressed) == 0:
                self.is_pressed = False
                # Starts the text2carbon phase
                Clipboard_to_image(theme, language, path).get_clipboard_text()

        except KeyError:
            pass

# This class gets the text from your clipboard, turns it into a carbon image and then copys it to your clipboard
class Clipboard_to_image():
    # Getting the variables for looks and filepath
    def __init__(self, theme, language, path):
        self.theme = theme
        self.language = language
        self.path = path

    # Copying the saved image to clipboard
    def add_clipboard(self, path):
        # grabbing image from path of image
        image = Image.open(path)
    
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()  
        
        # copying image to clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)    
        win32clipboard.CloseClipboard()

    # Getting clipboard data
    def get_clipboard_text(self):
        # get clipboard text
        self.send_request(pyperclip.paste())
    
    # Sending requests with image info to carbonara then saving file in filepath
    def send_request(self, text):
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
        path = f"{self.path}/{str(name)}.png"
        # sending request
        resp = requests.post(url_carbonara, headers=headers, json=data)

        # saving file
        open(path, 'wb').write(resp.content)
        self.add_clipboard(path)