import dweepy
import time
import pyodbc

def getLatestDweet(thingName):
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=Naimi\SQLEXPRESS;'
                        'Database=IoT;'
                        'UID=drabula;'
                        'PWD=minh03dz;'
                        'Trusted_Connection=yes;'
                        )
    cursor = conn.cursor()
    last_time = ""

    url = dweepy.get_latest_dweet_for(thingName)
    dict = url[0]
    longdate = dict['created']
    date = longdate[:10] 
    timeStamp = longdate[11:19] 
    t = dict['content']["Temperture"] 
    h = dict['content']["Humidity"]
    n = dict['content']["Sound"]
    g = dict['content']["Gas"] 
    l = dict['content']["Light"]

    sql = "INSERT INTO IoT_2 (Device_name, Time, temperture, humidity, gas, sound, light) VALUES (?, ?, ?, ?, ?, ?, ?)"
    val = (str(thingName), str(date), str(t), str(h), str(n), str(g), str(l))
    cursor.execute(sql, val)
    conn.commit()
    last_time = longdate
    print(val)

def main():
    thingName = "nhom9"
    max_iterations = 100
    count = 0

    while count < max_iterations:
        count += 1
        print("Count =", count)
        getLatestDweet(thingName)

    stop = input("Kết thúc (y/n)? ")
    if stop == "y":
        print("Main thread finished.")

if __name__ == "__main__":
    main()