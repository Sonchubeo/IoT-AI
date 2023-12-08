import dweepy
from threading import Event
import time
import pyodbc
from threading import Thread, Event
from urllib import request
    
def getLatestDweet_Thread(thingName, event):
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=Naimi\SQLEXPRESS;'
                        'Database=IoT;'
                        'UID=drabula;'
                        'PWD=minh03dz;'
                        'Trusted_Connection=yes;'
                        )
    cursor = conn.cursor()
    last_time = ""
    while not event.is_set():
        url = dweepy.get_latest_dweet_for(thingName)
        dict = url[0]
        longdate = dict['created']
        date = longdate[:10] 
        timeStamp = longdate[11:19] 
        t = dict['content']["Temperture"] 
        h = dict['content']["Humidity"]
        n = dict['content']["Gas"]
        g = dict['content']["Sound"] 
        l = dict['content']["Light"]
        if last_time != longdate:
            sql = "INSERT INTO IoT (Device_name, Time, Temperture, Humidity,  Gas,  Sound,  Light) VALUES (?, ?, ?, ?, ?, ?, ?)"
            val = (str(thingName), str(date), str(t), str(h), str(n), str(g), str(l))
            cursor.execute(sql, val)
            conn.commit()
            last_time = longdate
        print(sql)
        print(val)
        time.sleep(3)

def stopGetDataDweet_Thread(event):
    event.set()

#Create an Event object
event = Event()

#Create and start the file download thread
getdata_thread = Thread(target=getLatestDweet_Thread, args=("nhom9", event))
getdata_thread.start()

count = 0
while(count < 3):
    count += 1
    print("Count =", count)
    time.sleep(1)

stop = input("Kết thúc (y /n)? ")
if stop == "y":
    print("Main thread finished.")
    event.set()
   # DBCC CHECKIDENT ('dbo.IoT_1', RESEED, 1);