#!/usr/bin/env python

# use commands of the OS and terminal in programs
import subprocess

# Let the user parse the program and the commands in terminal line at once
import optparse

# import module for regular expressions
import re

def get_arguments():
    # parser object to handle user input
    parser = optparse.OptionParser()
    # this instance will handle the user input (-i or --interface to start)
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# first we capture options and arguments with get arguments
options = get_arguments()

# then we call the function
# change_mac(options.interface, options.new_mac)

# capture the value of the interface with check_output
ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
print(ifconfig_result)

# search ifconfig_result to capture only mac address with regular expressions
# thanks to pythex.org
mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

# check if the interface has a mac
if mac_address_search_result:
    # print only the first result with group(0)
    print(mac_address_search_result.group(0))
else:
    print("[-] Could not read MAC address")


