#!/usr/bin/env python

# goal : discover all clients in the same network with arp

# this version is optimized for python 3

# Let the user parse the program and the commands in terminal line at once
# import optparse (depricated)
import argparse

# needs to be imported in settings in pycharm
import scapy.all as scapy

# you need to install (pip install scapy-python3) install for python2
# you need to install (pip3 install scapy-python3) for python3


# take arguments from command line
def get_arguments():
    # parser object to handle user input
    parser = argparse.ArgumentParser()
    # this instance will handle the user input (-i or --ip_address to start)
    parser.add_argument("-t", "--target", dest="target", help="give target ip with range ex 10.0.2.1/24")
    (options) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an ip, use --help for more info.")
    else:
        return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    #initite an empty list
    clients_list =[]
    for element in answered_list:
        # for each element create a dictionary
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        # append the dict in the initiated list
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n--------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


# first we capture options and arguments with get arguments
options = get_arguments()

# store scan result from scan function execution
scan_result = scan(options.target)
# then we call the print function with the above saved result
print_result(scan_result)

