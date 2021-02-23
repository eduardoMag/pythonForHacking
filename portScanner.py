import socket
import subprocess
import sys
from datetime import datetime

#clear screen
subprocess.call('', shell=True)

#ask for input
remoteServer = input("Enter a remote host to scan: ")
remoteServerIp = socket.gethostbyname(remoteServer)

#print a banner with information on which host we are about to scan
print("-" * 60)
print("Please wait. Scanning remote host " + remoteServerIp)
print("-" * 60)

#check what time the scan started
t1 = datetime.now()

#using the range function to specify ports
#including error handling for error catching
try:
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIp, port))
        if result == 0:
            print("Port {}: Open".format(port))
        sock.close()

except KeyboardInterrupt:
    print("You pressed Ctrl+C")
    sys.exit()

except socket.gaierror:
    print("hostname could not be resolved. Exiting")
    sys.exit()

except socket.error:
    print("Could not connect to server")
    sys.exit()

#check time again
t2 = datetime.now()

#calculate difference of time, to see how long it took to run script
total = t2 -t1

#printing the information to screen
print("Scanning completed in " + total)
