from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
from scapy.volatile import RandMAC


# interface to use to send beacon frames, must be in monitor mode
iface = "wlan0mon"
# gerate a random MAC address (built-in in scapy)
sender_mac = RandMAC()
# SSID (name of access point
ssid = "Test"
# 802.11 frame
dot11 = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=sender_mac, addr3=sender_mac)
# beacon layer
beacon = Dot11Beacon()
# putting ssid in the frame
essid = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
# stack all the layers and add a RadioTap
frame = RadioTap()/dot11/beacon/essid
# send the frame in layer 2 every 100 milliseconds forever
# using the `iface` interface
sendp(frame, inter=0.1, iface=iface, loop=1)
"""
We generate a random MAC address as well as setting a name of our access point we want to create and then we create a 802.11 frame, the fields are:

type=0:  indicates that it is a management frame.
subtype=8:  indicates that this management frame is a beacon frame.
addr1: refers to the destination MAC address, in other words, the receiver's MAC address, we use the broadcast address here ("ff:ff:ff:ff:ff:ff"), if you want this fake access point to appear only in a target device, you can use the target's MAC address.
addr2: source MAC address, the sender's MAC address.
addr3: the MAC address of the access point.
"""
