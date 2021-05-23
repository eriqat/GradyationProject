#!/usr/bin/env python

import subprocess
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    # "optparse" is created as an instance of the option parser class which is an object that can handle parsing
    # we're giving "parser" the arguments that it can expect from users
    parser.add_option("-n", dest="command_num", help="number of the function listed ")
    # dst is the name where the value of the interface is going to be stored.

    # we're going to tell this child to parse the arguments that it gets from the user.
    # "options"  this is what contains the values that the user
    # inputs to access the value for the interface name and the mac address
    # "arguments" variable is going to contain the arguments.
    (options, arguments) = parser.parse_args()

    # way to check and make sure that the user entered a value for the interface and also entered
    # a value for the Mac
    if not options.command_num:
        parser.error("[-] please specify an integer number .. , use --help for more info")
    return options


# command_num = get_arguments()

def get_command_number(command_num):
    if command_num == 1:
        command = "python mac.changer.py"
        return command
    elif command_num == 2:
        command = "python network_scanner.py"
        return command
    elif command_num == 3:
        command = "python arp_spoof.py"
        return command
    elif command_num == 4:
        command = "python packet_sniffer.py"
        return command
    elif command_num == 5:
        command = "python net_cut.py"
        return command
    elif command_num == 6:
        command = "python replace_downloads.py"
        return command


print("1- MAC changer \n2- Network scanner \n3- ARP spoofer "
      "\n4- packet sniffer \n5- DNS spoofer \n6- file interceptor "
      "\n7- code injection")

options = get_arguments()
command = get_command_number(options.command_num)
subprocess.Popen(command, shell=True)

