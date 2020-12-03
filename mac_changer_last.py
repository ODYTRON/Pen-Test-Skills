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


def get_current_mac(interface):
    # capture the value of the interface with check_output
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # search ifconfig_result to capture only mac address with regular expressions
    # thanks to pythex.org
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    # check if the interface has a mac
    if mac_address_search_result:
        # print only the first result with group(0)
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


# first we capture options and arguments with get arguments
options = get_arguments()
# get current mac
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

# then we call the function change the mac
change_mac(options.interface, options.new_mac)


# get current mac
current_mac = get_current_mac(options.interface)
# check if the current_mac is the same that the user requested
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")




