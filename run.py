import main

if __name__ == '__main__':
    text_to_image = main.Clipboard_to_image(main.theme, main.language, main.path)
    key_listener = main.Keyboard_listener(main.keybind)
    input()