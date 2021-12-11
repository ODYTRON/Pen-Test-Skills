#!/usr/bin/env python
import scapy.all as scapy


def sniff(interface):
    # prn is the callback function which reads every packet of the interface we want to sniff
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)



def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        print(packet.show())








sniff("eth0")


# with packet.show(you can determine the fields of a layer you want to filter example row and HTTPrequest)
# print(packet.show())
# print(packet)

#SOS SOS SOS #
# EXAMPLE
# print(packet[scapy.YOURLAYER].YOURFIELD)
# print(packet[scapy.Raw].load)
