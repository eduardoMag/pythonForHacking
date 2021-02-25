import requests

# domain to scan for subdomains
domain = "google.com"

# read all subdomains
file = open("common-subdomains.txt")

# read all content
content = file.read()

# split by new lines
subdomains = content.splitlines()

# list of discovered subdomains
discovered_subdomains = []
for subdomain in subdomains:
    # construct the url
    url = f"http://{subdomain}.{domain}"
    try:
        # if this raises an error, that means subdomain does not exist
        requests.get(url)
    except requests.ConnectionError:
        # if the subdomain does no exit just pass
        pass
    else:
        print("[*] Discovered subdomain: ", url)
        # append the discovered subdomain to our list
        discovered_subdomains.append(url)

# save discovered subdomains into a file
with open("discovered_subdomainsTest1.txt", "w") as f:
    for subdomain in discovered_subdomains:
        print(subdomain, file=f)
