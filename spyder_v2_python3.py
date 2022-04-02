#!/usr/bin/env python

import requests
import re
# urlparse for python3
import urllib.parse as urlparse



target_url = "https://zsecurity.org"
# empty list to feed it later
target_links = []  

def extract_links_from(url):
    response = requests.get(url)
    # CAST BYTE TO STRING OR .decode() IT excluding all the errors
    
    # return re.findall('(?:href=")(.*?)"', str(response.content))
    
    # or
    
    return re.findall('(?:href=")(.*?)"', str(response.content.decode(errors="ignore")))
    

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        # convert relative urls to full urls
        link = urlparse.urljoin(url, link)
        
        # exclude same links with diffrent content on  the same page
        if '#' in link:
            link = link.split("#")[0]
        
        # exclude links outside the target url and remove duplicate links of the page
        if target_url in link and link not in target_links:
            # put links in the list
            target_links.append(link)
            print(link)
            # keep exploring the links of the menus recursively by calling the function itself
            # it navigates into existing links for more links on the same page and not only the home page
            crawl(link)

crawl(target_url)
