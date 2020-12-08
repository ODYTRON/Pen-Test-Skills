#!/usr/bin/env python

# goal : discover all clients in the same network

# needs to be imported in settings in pycharm
import scapy.all as scapy


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    # scapy.ls(scapy.ARP()) just to see the list of arguments that ARP takes
    # arp_request.pdst=ip you can also call the argument in ARP look above
    # print(arp_request.summary()) have the summary of arp request

    # create an ethernet frame (ethernet object) for the mac address communicaton (physical connection layer two)
    # you need to broadcast this mac address to all devices
    # aka set destination MAC to broadcast MAC you can set specific MAC If you want
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary()) have the summary which sends a packet from my mac to all (broadcast)
    # then you have to combine two requests together
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.summary())
    # with show() we see more details of a packet who sends what examples in last line
    # arp_request_broadcast.show()
    # send and recieve function the response with values in two vars : answered and unanswered packets
    # answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout = 1)
    # print(answered_list.summary())
    # print(unanswered_list.summary())
    # capture only the  first element of the list (answered_list)
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    print(answered_list.summary())
    # access elements of the list individually
    print("IP\t\t\tMAC Address\n--------------------------------------------------")
    for element in answered_list:
        # the element has two subelements: the request sent and  the answer [0],[1]
        # to print apropriate fields use .show()
        print(element[1].psrc + "\t\t" + element[1].hwsrc)





scan("10.0.2.1/24")

########################### show(examples) who sends what
# arp_request.show()
# broadcast.show()
# arp_request_broadcast.show()