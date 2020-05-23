# Checking ICMP reachability to devices referenced by Excel file in format (Node_IP_address, Node_name, Node_owner)
# Stupid task automation 
# Bogdan Adrian Burciu 22/05/2020 vers 1

# -------------------------
# Credits: 
# https://dev.to/ankitdobhal/let-s-ping-the-network-with-python-scapy-5g18
# https://stackoverflow.com/questions/25980777/new-to-scapy-trying-to-understand-the-sr
# https://thepacketgeek.com/scapy-p-06-sending-and-receiving-with-scapy/
# https://stackoverflow.com/questions/14931906/extract-columns-from-excel-using-python
# https://stackoverflow.com/questions/3389574/check-if-multiple-strings-exist-in-another-string

from scapy.all import *
import xlrd
from termcolor import colored   # to be able to color text in console, method colored()

sh = xlrd.open_workbook('/root/Downloads/4thFloorLab.xlsx').sheet_by_index(0) 
ips = sh.col_values(0, start_rowx=0)
names = sh.col_values(1, start_rowx=0)
reps = sh.col_values(2, start_rowx=0)  # <== lists of all values in 3rd column (#2, first being #0) of input .xlsx
probl = open("/root/Downloads/ProblematicNodes.txt", 'w+')

vmatch = ["VM", "CloudLens", "centos", "CentOS", "ANVL", "VLM"]	   # exclude nodes from ICMP test if their  names containt these values 
reps_dict={}    # a dict of key=representative/owner and value=len(dict) mod 7, so that each rep gets associated a sticky value 
colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]

for i in range(len(names)):
	if any(x in str(names[i]) for x in vmatch):   # check if multiple strings exist in another string, use "all" instead of "any" if needed to verify all at once
 		continue
	else:
		print(f"Checking host {ips[i]}")  
		pkt=sr1(IP(dst=ips[i])/ICMP(),timeout=2)
		if pkt == None:
			if len(reps[i])==0 :
				reps[i]="no_owner_registered"    # when there's no representative/owner (no value in input .xlsx in 3rd column), replace it 

			if reps[i] in reps_dict:
				print(colored(f"The host {ips[i]}:'{names[i]}' is down. Node owner '{reps[i]}', please help on-site resources with node's physical position.", colors[reps_dict[reps[i]]]))
				probl.write(colored(f"The host {ips[i]}:'{names[i]}' is down. Node owner '{reps[i]}', please help on-site resources with node's physical position.\n", colors[reps_dict[reps[i]]] ) )
			else:
				reps_dict[reps[i]]=len(reps_dict)%7	# dict of key=rep/owner and value=0..6
				print(colored(f"The host {ips[i]}:'{names[i]}' is down. Node owner '{reps[i]}', please help on-site resources with node's physical position.", colors[reps_dict[reps[i]]] ))
				probl.write(colored(f"The host {ips[i]}:'{names[i]}' is down. Node owner '{reps[i]}', please help on-site resources with node's physical position.\n", colors[reps_dict[reps[i]]]))

probl.close()

# -------------------------
# >>> from scapy.all import *
# >>> p=sr(IP(dst="10.38.161.65")/ICMP(),timeout=2)
# Begin emission:
# ....Finished sending 1 packets.
# *
# Received 5 packets, got 1 answers, remaining 0 packets
# >>>
# >>> IPadresa="10.38.161.64"
# >>> p=sr(IP(dst=IPadresa)/ICMP())
# Begin emission:
# ...Finished sending 1 packets.
# *
# Received 4 packets, got 1 answers, remaining 0 packets
# >>>
# Scapy generated frame:

# Frame 489: 42 bytes on wire (336 bits), 42 bytes captured (336 bits) on interface \Device\NPF_{62A356FA-03FF-4F6D-BDC3-0F778786F985}, id 0
# Ethernet II, Src: Cisco_3c:7a:00 (00:05:9a:3c:7a:00), Dst: CIMSYS_33:44:55 (00:11:22:33:44:55)
# Internet Protocol Version 4, Src: 10.22.219.99, Dst: 10.38.161.65
# Internet Control Message Protocol
    # Type: 8 (Echo (ping) request)
    # Code: 0
    # Checksum: 0xf7ff [correct]
    # [Checksum Status: Good]
    # Identifier (BE): 0 (0x0000)
    # Identifier (LE): 0 (0x0000)
    # Sequence number (BE): 0 (0x0000)
    # Sequence number (LE): 0 (0x0000)
    # [No response seen]
        # [Expert Info (Warning/Sequence): No response seen to ICMP request]
            # [No response seen to ICMP request]
            # [Severity level: Warning]
            # [Group: Sequence]

# -------------------------
# >>> from termcolor import colored
# >>> help(colored)
# Help on function colored in module termcolor:

# colored(text, color=None, on_color=None, attrs=None)
    # Colorize text.
    
    # Available text colors:
        # red, green, yellow, blue, magenta, cyan, white.
    
    # Available text highlights:
        # on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.
    
    # Available attributes:
        # bold, dark, underline, blink, reverse, concealed.

