#!/bin/bash 
# cp ScanLAN.sh /usr/local/bin 
export GREEN=$(tput setaf 2 :-"" 2>/dev/null)

if ! command -v figlet &> /dev/null
then
    echo "Installing packages - Please wait!"
    sudo apt-get install -y figlet 
fi
figlet Scan the LAN!
echo "Declaimer!"
echo "This tool is for educational purpose only! the author is not resposible for any iligale usage."
echo "authoerd by Abu AL-Zait AND Sami"
echo $GREEN;printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
echo "Please choose what you whant to do with your LAN!"
echo "1) Network Scanner"
echo "2) ARP Spoofer"
echo "3) Packet Sniffer"
echo "4) DNS Spoofer"
echo "5) File Interceptor"
echo "6) code Injector"
echo "7) MAC Changer"
echo "0) Exit!"
echo "Enter option between [1-7]:"
read  input
if [ $input -eq 1 ]
then
    echo "enter the ip range to scan ..."
    read ip
    echo -e
    python network_scanner.py --ip=$ip
    echo -e
    sleep 5 
elif [ $input -eq 2 ]
then
    echo "enter the ip of the gateway..."
    read ip1
    echo "enter the ip of the victim..."
    read ip2
    echo -e
   python arp_spoof.py -g $ip1 -v $ip2
elif [ $input -eq 3 ]
then 
    echo "enter the name of the interface :  "
   read interface 
   python packet_sniffer.py --i $interface
elif [ $input -eq 4 ]
then 
   python dns_spoofer.py
elif [ $input -eq 5 ]
then 
   echo "enter the replacing link insted of download ... "
   read address
   python replace_downloads.py --a $address
elif [ $input -eq 6 ]
then 
   python coode_injector.py
elif [ $input -eq 7 ]
then 
    echo "enter the interface"
    read i
    echo "enter the new mac" 
    read m
    python mac.changer.py -i $i -m $m
    echo -e
    sleep 5
elif [ $input -eq 0 ]
then
echo "bye!" 
exit
else 
echo "you entered wrong number!"
# bash ScanLAN.sh
fi
