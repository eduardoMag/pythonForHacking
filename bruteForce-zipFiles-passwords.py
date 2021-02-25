import zipfile
from tqdm import tqdm

# password list path to use (must be in same directory)
wordlist = "rockyou.txt"

# zip file to crack
zip_file = "secret_flag.zip"

# initialize the zip file object
zip_file = zipfile.ZipFile(zip_file)

# count the number of words in this wordlist
n_words = len(list(open(wordlist, "rb")))

# print the total of number of passwords
print("Total passwords to test:", n_words)

with open(wordlist, "rb") as wordlist:
    for word in tqdm(wordlist, total=n_words, unit="words"):
        try:
            zip_file.extractall(pwd=word.strip())
        except:
            continue
        else:
            print("[+] Password found: ", word.decode().strip())
            exit(0)
print("[!] Password not found, try other wordlist.")
