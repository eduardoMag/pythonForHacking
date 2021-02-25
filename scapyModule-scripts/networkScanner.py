from scapy.all import srp
from scapy.layers.l2 import ARP, Ether

# ip address for the destination
target_ip = "127.0.0.1/24"

# create ARP packet
arp = ARP(pdst=target_ip)

# create the ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# stack them
packet = ether / arp

# set timeout to 3 to prevent script clogging
result = srp(packet, timeout=3)[0]

# list of clients, fill with loop
clients = []

for sent, received in result:
    # for each response, append ip and mac address to clients
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network: ")
print("IP" + ""*2 + "MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))
