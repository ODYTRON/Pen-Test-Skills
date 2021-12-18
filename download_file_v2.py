#!/usr/bin/env python
import requests
def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    # print(file_name)
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("https://cdn.cnngreece.gr/media/news/2021/12/17/293908/main/visual-stories-micheile--DhNe1P1C0A-unsplash.jpg")
