#!/bin/bash

from plyer import notification
import speedtest
import netifaces
from datetime import datetime
import os
import time as t
import urllib.request

def ip():
    gws = netifaces.gateways()
    ip = gws['default'][netifaces.AF_INET][0]
    file = open('expo_Networking_logs.txt','a')
    file.write("\n Gateway ip "+ip)
    file.close()
    global host
    host = "http://"+ ip + "/"

def connect():
    try:
        ip()
        urllib.request.urlopen(host) 
        return True
    except:
        return False

def internet(host='https://fast.com/'):
    try:
        urllib.request.urlopen(host) 
        return True
    except:
        return False

def notify2():
    title = "expo-Net"
    notification.notify(title= title,
                    message= notify,
                    app_icon = None,
                    timeout= 10,
                    toast=False)

global notify
speed =0
e2 = 0
lim = 0
iA = 0
file = open('expo_Networking_logs.txt','w')
file.write("")
file.close()
while True:
    
    if connect() == False:
        now = datetime.now()
        file = open('expo_Networking_logs.txt','a')
        file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
        if internet() == True:
            file.write(" Error_1 !!")
            file.close()
            if e2 >= 5:
                t.sleep(60)
                
        else:
            file.write(" Not Connected     No Internet Access")
            file.close()
        
            if lim >= 5:
                file = open('expo_Networking_logs.txt','a')
                file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
                file.write(" Error_2 !!")
                file.close()
                notify = "Error in Connecting...retrying in 60s"
                notify2()
            
                t.sleep(60)
            else:
                os.system("sudo nmcli networking off")
                t.sleep(1)
                os.system("sudo nmcli networking on")
                lim += 1
                file = open('expo_Networking_logs.txt','a')
                file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
                file.write(" Reconneting...")
                file.close()
                t.sleep(5)
                
    else:

        lim = 0
        e2 = 0
        now = datetime.now()
        file = open('expo_Networking_logs.txt','a')
        file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
        if internet() == True:
            iA += 1
            file.write(" Connected     Internet Access")
            if iA == 1:
                 st = speedtest.Speedtest()
                 speed = ((round(st.download()/1048576) + round(st.download()/1048576))/2)

                 file.write("\n Internet Speed "+str(speed)+"Mbits")
                 if speed < 10:
                    notify = "Your Internet Connection is slow"
                    notify2()
                
            file.close()
        else:
            file.write(" Connected     No Internet Access")
            file.close()
    
        t.sleep(5)

        
