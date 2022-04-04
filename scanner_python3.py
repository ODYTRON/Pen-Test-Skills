#!/usr/bin/env python

import requests
import re
# urlparse for python3
import urllib.parse as urlparse
# beautiful soup in python3
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url, ignore_links):
        # create sessions (persist) to stay logged in (in every request you have to call self.session)
        # if you logged in you will have more things to explore (links, etc)
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = ignore_links
        
    def extract_links_from(self, url):
        response = self.session.get(url)
        # .decode() to run in python3
        return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore")

    def crawl(self, url=None):
    
        if url == None:
            url = self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            # convert relative urls to full urls
            link = urlparse.urljoin(url, link)
            
            # exclude same links with diffrent content on  the same page
            if '#' in link:
                link = link.split("#")[0]
            
            # exclude links outside the target url and remove duplicate links of the page and ignore logout links
            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                # put links in the list
                self.target_links.append(link)
                print(link)
                # keep exploring the links of the menus recursively by calling the function itself
                # it navigates into existing links for more links on the same page and not only the home page
                self.crawl(link)
    

    def extract_forms(self, url):
        response = self.session.get(url)
        # get the html content
        print(response.content)
        # parse html content using beautifuloup 
        parsed_html = BeautifulSoup(response.content) 
        # get all forms
        return parsed_html.findall("form")
        
        
    def submit_form(self, form, value, url):
        action = form.get("action")
        # transform the action url from relative to full url
        post_url = urlparse.urljoin(url, action)
        print(post_url)
        print(action)
        method = form.get("method")
        print(method)
    
        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            input_name = input.get("name")
            print(input_name)
            # get the type , you need all text type fields to send your payload
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value
            
            post_data[input_name] = input_value
        if method == "post":
            # submit the form with the test data in items
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)
        
        
    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss:
                    print("\n\n[***] XSS discovered in" + link "in the following form")
                    print(form)
                
            if "=" in link:
                print("\n\n[+] Testing " + link)
                is_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                print("[***] discovered XSS in" + link)
                
                
    def test_xss_in_link(self, url):
        xss_test_script = "<sCript>alert('na tos o kontos')</scriPt>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        if xss_test_script.encode() in response.content:
            return True
    
                
    def test_xss_in_form(self, form, url):
        xss_test_script = "<sCript>alert('na tos o kontos')</scriPt>"
        response = self.submit_form(form, xss_test_script, url)
        # encode() to convert a string to a byte like object to run with python3
        if xss_test_script.encode() in response.content:
            return True
                
        
        
    
        