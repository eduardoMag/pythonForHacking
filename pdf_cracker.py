import pikepdf
from tqdm import tqdm


# load password list
passwords = [line.strip() for line in open("simple_wordlist.txt")]

# iterate over passwords
for password in tqdm(passwords, "Decrypting PDF"):
    try:
        # open PDF file
        with pikepdf.open("file_to_decrypt.pdf", password=password) as pdf:
            # password decrypted successfully, break out of loop
            print("[+] Password found:", password)
            break
    except pikepdf._qpdf.PasswordError as e:
        # wrong password, just continue loop
        continue
