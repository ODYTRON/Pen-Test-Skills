#!/bin/python

import sys
import socket
from datetime import datetime

# Define our target

if len(sys.argv) == 2:
    # translate hostname to IPv4 the format of args is : python3 port_scanner.py <ip>
    target = socket.gethostbyname(sys.argv[1])
else:
    print("invalid amount of arguments")
    print("format must be : python3 port_scanner.py <ip or HOST name>")

# Add a banner to the program
print("-" * 50)
print("Scanning target" + target)
print("Time started:" + str(datetime.now()))
print("-" * 50)

try:
    for port in range(0, 65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))  # returns an error indicator
        print("Checking port {}".format(port))
        if result == 0:
            print("Port {} is open".format(port))
        s.close()

except KeyboardInterrupt:
    print("\nExiting Program. ")
    sys.exit()

except socket.gaierror:
    print("Hostname could not be resolved. ")
    sys.exit()

except socket.error:
    print("Couldn't connect to server. ")
    sys.exit()








