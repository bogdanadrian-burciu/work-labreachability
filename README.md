# work-labreachability
Check if lab devices from an Excel file in format (Node_IP_address, Node_name, Node_owner) are reachable by ICMP.
I wrote this script due to problems with power outages in the office lab, causing different problems with reaching lab devices, while the team was in COVID-19 lockdown.
It allows for priorizing important nodes and their respective need for on-site checks.

Gets as input a .xslx file like row#1: 10.38.160.147	VMWare ESXi hypervisor host 6.7	  NVS Team, row#2: 10.38.160.43	kvm Bogdan Burciu.
Sends an ICMP request like below and checks received packets, using the Scapy library of Python3. If there is a reply (sr1() != None), means the node is IP reachable, hence alive.

>>> sr1(IP(dst='10.38.161.65')/ICMP(id=1, seq=13983),timeout=2)
Begin emission:
Finished sending 1 packets.
.*
Received 2 packets, got 1 answers, remaining 0 packets
<IP  version=4 ihl=5 tos=0x0 len=28 id=61843 flags= frag=0 ttl=60 proto=icmp chksum=0xfc6c src=10.38.161.65 dst=10.22.219.99 |<ICMP  type=echo-reply code=0 chksum=0xc95f id=0x1 seq=0x369f |>>

   Internet Protocol Version 4, Src: 10.22.219.99, Dst: 10.38.161.65
   Internet Control Message Protocol
       Type: 8 (Echo (ping) request)
       Code: 0
       Checksum: 0xc15f [correct]
       [Checksum Status: Good]
       Identifier (BE): 1 (0x0001)
       Identifier (LE): 256 (0x0100)
       Sequence number (BE): 13983 (0x369f)
       Sequence number (LE): 40758 (0x9f36)
       [Response frame: 4631]
 
 (Not using default values for ICMP, since my employer's corporate network probably has statefull inspection devices, like Firewalls or IDS, that does not allow such requests to reach the office lab).

 # How to run:
PS C:\Users\boburciu> python C:\Users\boburciu\Desktop\Automation_Python_for_Network_Engineers_by_David_Bombal\pingLabWin.py

 Please input absolute path to the file where unreachable nodes should be stored (like C:\Users\boburciu\Downloads\problematicNodes.docx):C:\Users\boburciu\Downloads\problematicNodes.docx
 Checking host 10.38.161.2
 Begin emission:
 Finished sending 1 packets.
 :
 :
 
 # Pre-requisites:
To use this script in Win PyCharm, you need the xlrd, scapy and docx modules installed, then Pycharm ALT+CRLS+S > Project Interpreter > + for modules
# PS C:\Users\boburciu> # pip3 install xlrd
 Collecting xlrd
   Downloading https://files.pythonhosted.org/packages/b0/16/63576a1a001752e34bf8ea62e367997530dc553b689356b9879339cf45a4
 /xlrd-1.2.0-py2.py3-none-any.whl (103kB)
      |████████████████████████████████| 112kB 726kB/s
 Installing collected packages: xlrd
 Successfully installed xlrd-1.2.0
 WARNING: You are using pip version 19.2.3, however version 20.1.1 is available.
 You should consider upgrading via the 'python -m pip install --upgrade pip' command.
 PS C:\Users\boburciu>
 # PS C:\Users\boburciu> # pip3 install scapy
 Requirement already satisfied: scapy in c:\users\boburciu\appdata\local\programs\python\python37-32\lib\site-packages\scapy-git_archive.devef60120dfb-py3.7.egg (git-archive.devef60120dfb)
 WARNING: You are using pip version 19.2.3, however version 20.1.1 is available.
 You should consider upgrading via the 'python -m pip install --upgrade pip' command.
 PS C:\Users\boburciu>
 # PS C:\Users\boburciu> # pip3 install python-docx	 # docx module is not for Python3
 Collecting python-docx
   Downloading https://files.pythonhosted.org/packages/e4/83/c66a1934ed5ed8ab1dbb9931f1779079f8bca0f6bbc5793c06c4b5e7d671/python-docx-0.8.10.tar.gz (5.5MB)
      |████████████████████████████████| 5.5MB 6.4MB/s
 Requirement already satisfied: lxml>=2.3.2 in c:\users\boburciu\appdata\local\programs\python\python37-32\lib\site-packages (from python-docx) (4.5.1)
 Installing collected packages: python-docx
   Running setup.py install for python-docx ... done
 Successfully installed python-docx-0.8.10
 WARNING: You are using pip version 19.2.3, however version 20.1.1 is available.
 You should consider upgrading via the 'python -m pip install --upgrade pip' command.
