#!/bin/bash 
figlet Scan the LAN!
echo "Declaimer!"
echo "This tool is for educational purpose only! the author is not resposible for any iligale usage."
echo "authoerd by Abu AL-Zait"
echo "----------------------------------------------------------------------------------------------" 
echo "Please choose what you whant to do with your LAN!"
echo "1) MAC Changer"
echo "2) Network Scanner"
echo "3) ARP Spoofer"
echo "4) Packet Sniffer"
echo "5) DNS Spoofer"
echo "6) File Interceptor"
echo "7) Code Injectore"
echo "Enter option between [1-7]:"
read  input
if [ $input -eq 1 ]
then
    python mac.changer.py 
elif [ $input -eq 2 ]
then 
   python network_scanner.py 
elif [ $input -eq 3 ]
then 
   python arp_spoof.py 
elif [ $input -eq 4 ]
then 
   python packet_sniffer.py 
elif [ $input -eq 5 ]
then 
   python net_cut.py 
elif [ $input -eq 6 ]
then 
   python replace_downloads.py 
elif [ $input -eq 7 ]
then 
   python code_injector.py 
else 
echo "you entered wrong number!"
fi
