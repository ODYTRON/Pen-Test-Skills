#!/usr/bin/env python
import requests
def download(url):
    get_response = requests.get(url)
    print(get_response)
    print(get_response.content)
    with open("sample.txt", "w") as out_file:
        out_file.write("this is a test")


download("https://cdn.cnngreece.gr/media/news/2021/12/17/293908/main/visual-stories-micheile--DhNe1P1C0A-unsplash.jpg")
