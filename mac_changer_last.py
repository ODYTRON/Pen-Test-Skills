#!/usr/bin/env python

# use commands of the OS and terminal in programs
import subprocess

# Let the user parse the program and the commands in terminal line at once
import optparse

def get_arguments():
    # parser object to handle user input
    parser = optparse.OptionParser()

    # this instance will handle the user input (-i or --interface to start)
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    return parser.parse_args()


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# first we capture options and arguments with get arguments
(options, arguments) = get_arguments()

# then we call the function
change_mac(options.interface, options.new_mac)

