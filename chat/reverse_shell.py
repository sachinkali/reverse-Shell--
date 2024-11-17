#!/usr/bin/python3
import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(("127.0.0.1",54321))
print("Connection Established to server")
while True:
 message=sock.recv(1024).decode()
 print(message)
 if message=='q':
  break
 else:
  answer=(input("Enter message to send: "))
  sock.send(answer.encode())
sock.close()
