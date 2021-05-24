#!/usr/bin/env python

import netfilterqueue


# implementation of the callback fucntion (do not be scared we use it afterwards)

def process_packet(packet):
    print(packet)
    # accept or drop the packets of the queue
    # packet.accept()
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

# after all

# iptables --flush




