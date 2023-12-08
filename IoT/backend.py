import requests
import time
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import datetime
import pytz
from check import checkStatus
#from check import dataBase
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Cấu hình thông tin Dweet và Thing của bạn
THING_NAME = "nhom9"
DWEET_URL = f"https://dweet.io/get/latest/dweet/for/{THING_NAME}"

# Biến lưu trữ thời gian lần cuối cùng
last_time = None

# Hàm lấy dữ liệu từ Dweet và đọc
def get_data_from_dweet():
    global last_time
    
    try:
        response = requests.get(DWEET_URL)
        data = response.json()
        response.close()
        
        # Truy cập dữ liệu từ Dweet ở đây
        created = data["with"][0]["created"]
        
        # Kiểm tra nếu thời gian mới lấy từ Dweet trùng với thời gian lần cuối cùng, bỏ qua xử lý dữ liệu
        if created == last_time:
            print("Skipping duplicate data.")
            return
        
        # Cập nhật thời gian lần cuối cùng
        last_time = created
        
        # Trích xuất ngày và giờ từ chuỗi "created"
        datetime_str = created[:-5]
        # Chuyển đổi múi giờ từ UTC sang múi giờ Hà Nội (UTC+7)
        utc_time = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
        hanoi_time = utc_time + datetime.timedelta(hours=7)
        
        # Định dạng lại thời gian theo định dạng mong muốn (VD: "%d/%m/%Y %H:%M:%S")
        hanoi_time_string = hanoi_time.strftime("%d/%m/%Y %H:%M:%S")
        
        # Chuyển chuỗi thành đối tượng datetime
        temperature = data["with"][0]["content"]["Temperture"]
        humidity = data["with"][0]["content"]["Humidity"]
        gas = data["with"][0]["content"]["Gas"]
        sound = data["with"][0]["content"]["Sound"]
        light = data["with"][0]["content"]["Light"]

        # Sử dụng dữ liệu từ Dweet
        print("Temperture:", temperature)
        print("Humidity:", humidity)
        print("Gas:", gas)
        print("Sound:", sound)
        print("Light:", light)
        print(hanoi_time_string)
       
        x = checkStatus(temperature, humidity, gas, sound, light)
        print("Dữ liệu thuộc tình huống:", x)
     #   dataBase(temperature, humidity, gas, sound, light, x,hanoi_time_string)

    except Exception as e:
        print("Failed to get data from Dweet:", e)

while True:
    # Gọi hàm để lấy và đọc dữ liệu từ Dweet
    get_data_from_dweet()
    time.sleep(1)