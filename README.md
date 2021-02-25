# pythonForHacking
simple scripts written in python for hacking.

[+] NOTE:
***FOR SCRIPT 'wifi-disconnect-devices' in scapyModule***
You can also set "ff:ff:ff:ff:ff:ff" (broadcast MAC address ) as addr1 (target_mac) and this will cause a complete denial of service, as no device can connect to that access point, this is quite harmful!

[+]Note:
***FOR SCRIPT 'DNS-spoof-attack' in scapyModule***
In order to be a man-in-the-middle, you need to execute the ARP spoof script, so the victim will be sending the DNS requests to your machine first, instead of directly routing them into the Internet.