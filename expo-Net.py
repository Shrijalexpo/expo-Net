import os
from gi.repository import Notify, GdkPixbuf
import speedtest
import netifaces
from datetime import datetime
import os
import time as t
import urllib.request


def ip():
    gws = netifaces.gateways()
    ip = gws['default'][netifaces.AF_INET][0]
    file = open('expo-Net-logs.txt', 'a')
    file.write("\n Gateway ip " + ip)
    file.close()
    global host
    host = "http://" + ip + "/"


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


def notify():
    Notify.init("expo-Net")
    summary = "expo-Net"
    notification = Notify.Notification.new(summary, msg)
    #file_name = os.getcwd + "/icon.jpg"
    #image = GdkPixbuf.Pixbuf.new_from_file(file_name)
    #notification.set_icon_from_pixbuf(image)
    #notification.set_image_from_pixbuf(image)
    notification.set_urgency(2)
    notification.show()


global msg
speed = 0
e2 = 0
lim = 0
iA = 0
file = open('expo-Net-logs.txt', 'w')
file.write("")
file.close()
while True:

    if connect() == False:
        now = datetime.now()
        file = open('expo-Net-logs.txt', 'a')
        file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
        if internet() == True:
            file.write(" Error_1 !!")
            file.close()
            if e2 >= 5:
                t.sleep(60)

        else:
            iA = 0
            file.write(" Not Connected     No Internet Access")
            file.close()

            if lim >= 5:
                file = open('expo-Net-logs.txt', 'a')
                file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
                file.write(" Error_2 !!")
                file.close()
                msg = "Error in Connecting...retrying in 60s"
                notify()

                t.sleep(60)
            else:
                os.system("sudo nmcli networking off")
                t.sleep(1)
                os.system("sudo nmcli networking on")
                lim += 1
                file = open('expo-Net-logs.txt', 'a')
                file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
                file.write(" Reconneting...")
                file.close()
                t.sleep(5)

    else:

        lim = 0
        e2 = 0
        now = datetime.now()
        file = open('expo-Net-logs.txt', 'a')
        file.write(now.strftime("\n %d/%m/%Y %H:%M:%S"))
        if internet() == True:
            iA += 1
            file.write(" Connected     Internet Access")
            if iA == 1:
                st = speedtest.Speedtest()
                speed = ((round(st.download() / 1048576) + round(st.download() / 1048576)) / 2)

                file.write("\n Internet Speed " + str(speed) + " Mbits")
                if speed < 20:
                    msg = "Your Internet Connection speed is slow"
                    notify()

            file.close()
        else:
            iA = 0
            file.write(" Connected     No Internet Access")
            file.close()

        t.sleep(5)
