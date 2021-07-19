import keyboard
import time
import pyperclip
import requests
import datetime
from io import BytesIO
import win32clipboard
from PIL import Image

keybind = "shift+windows+c"
theme = "panda"
language = "auto"
path = "C:/Users/Tom/OneDrive/Documents/Illustrator/PNG/carbon"

class Main():

    def __init__(self):
        pass
    
    def add_clipboard(self, name):
        image = Image.open(f"{path}{name}.png")
    
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()  

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def get_clipboard_text(self):
        # get clipboard data
        return pyperclip.paste()
    
    def send_request(self, text):
        url_carbonara = "https://carbonara.vercel.app/api/cook"
        headers = {"Content-Type": "application/json"}
        data = {"code":f"{text}",  "backgroundColor": "#1F816D"} #this can be whatever
        name = str(datetime.datetime.now())
        name = name.replace(".","-")
        name = name.replace(" ","_")
        name = name.replace(":","-")
        resp = requests.post(url_carbonara, headers=headers, json=data)
        #Make a directory where you want it to save the file then it can be handled later

        open(f"{path}{str(name)}.png", 'wb').write(resp.content)
        print("sent requests")
        return name

    def main(self):
        # loops program
        while True:
            if keyboard.is_pressed(keybind):    
                self.add_clipboard(self.send_request(self.get_clipboard_text()))
                time.sleep(2)