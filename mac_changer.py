#!/usr/bin/env python

import subprocess

# for python 2 instead of 3 the function is raw_input instead of input
interface = raw_input("interface > ")
new_mac = raw_input("NEW MAC ADDRESS > ")

print("[+] Changing MAC address for " + interface + "to " + new_mac)

subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
subprocess.call("ifconfig " + interface + " up", shell=True)
