# imports
import keyboard
import time
import pyperclip
import requests
import datetime
from io import BytesIO
import win32clipboard
from PIL import Image

# variables
keybind = "shift+windows+c"
theme = "panda"
language = "auto"
path = "C:/Users/Tom/OneDrive/Documents/Illustrator/PNG/carbon"

# main class
class Main():

    def __init__(self):
        pass
    
    def add_clipboard(self, name):
        # grabbing image from path of image
        image = Image.open(f"{path}{name}.png")
    
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
        return pyperclip.paste()
    
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
        # sending request
        resp = requests.post(url_carbonara, headers=headers, json=data)

        # saving file
        open(f"{path}{str(name)}.png", 'wb').write(resp.content)
        return name

    def main(self):
        # loops program
        while True:
            if keyboard.is_pressed(keybind):    
                self.add_clipboard(self.send_request(self.get_clipboard_text()))
                time.sleep(2)