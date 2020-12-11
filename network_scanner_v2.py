#!/usr/bin/env python

# goal : discover all clients in the same network with arp



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

    #initite an empty list
    clients_list =[]
    for element in answered_list:
        # for each element create a dictionary
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        # append the dict in the initiated list
        clients_list.append(client_dict)
    return clients_list
    # test final list outside loop it contains a list of dictionaries
    #print(clients_list)


def print_result(results_list):
    print("IP\t\t\tMAC Address\n--------------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" +client["mac"])
scan_result = scan("10.0.2.1/24")
print_result(scan_result)



########################### show(examples) who sends what
# arp_request.show()
# broadcast.show()
# arp_request_broadcast.show()