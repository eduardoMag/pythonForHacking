from scapy.all import *


sniff(prn=lambda x: send_response(x), lfilter=lambda x:x.haslayer(UDP) and x.dport == 53)
