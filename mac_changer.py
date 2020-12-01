#!/usr/bin/env python

# use commands of the OS and terminal in programs
import subprocess

# Let the user parse the program and the commands in terminal line at once
import optparse

# parser object to handle user input
parser = optparse.OptionParser()

# this instance will handle the user input (-i or --interface to start)
parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")

# for python 2 instead of 3 the function is raw_input instead of input
interface = raw_input("interface > ")
new_mac = raw_input("NEW MAC ADDRESS > ")

print("[+] Changing MAC address for " + interface + " to " + new_mac)


# call subprocess module to use call command first way
# seperated command calls

# subprocess.call("ifconfig " + interface + " down", shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
# subprocess.call("ifconfig " + interface + " up", shell=True)


############################################################################################

# call subprocess module to use call command second way
# more secure way to handle inputs and execute commands by putting our commands in lists
# by this way you have specific args that the program accepts
# so it is difficult for somebody to intercept our code.

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])
