#!/usr/bin/env python

import requests


def request(url):
    try:
        return get_response = requests.get("http://" + url)   
    except requests.exceptions.ConnectionError:
        pass

target_url = "10.0.2.20/mutillidae/"  
# common.txt from dirbuster to discover ULRS      
with open("/root/Downloads/common.txt.list", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] Discovered URL --> " + test_url) 
 