#!/usr/bin/env python

import requests
from BeautifulSoup import BeautifulSoup
import urlparse


def request(url):
    try:
        return get_response = requests.get(url)   
    except requests.exceptions.ConnectionError:
        pass
        

target_url = "http://10.0.0.2/multitadea"
response = requests(target_url)
# get the html content
print(response.content)

# parse html content using beautifuloup 
parsed_html = BeautifulSoup(response.content)

# get all forms
forms_list = parsed_html.findAll("form")

# access one element at the time and extract attributes from forms
for form in forms_list:
    action = form.get("action")
    # transform the action url from relative to full url
    post_url = urlparse.urljoin(target_url, action)
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
            input_value = "test"
            
        post_data[input_name] = input_value
        
    # submit the form with the test data in items
    result = requests.post(post_url, data=post_data)
    print(result.content)
    
        
        
        

