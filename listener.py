#!/usr/bin/python
import socket

# create a socket object  named listener
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# modify an option so that we can reuse sockets
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# instead of connecting to a destination we binding our socket to our computer so that we listen for incoming connections on port 4444
listener.bind(("192.168.1.2", 4444))

# the number of connections that can be cued before the connections start getting refused
listener.listen(0)

print("[+] Waiting for incoming connections")

# if you get a connection just accept it
listener.accept()

print("[+] Got a connection")