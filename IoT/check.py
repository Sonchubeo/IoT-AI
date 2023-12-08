import pyodbc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Tải mô hình đã huấn luyện
model = load_model('my_model.keras')

# Tải trọng số của mô hìnhS
model.load_weights('my_weights.keras')
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Kết nối đến cơ sở dữ liệu
try:
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=Naimi\SQLEXPRESS;'
                        'Database=IoT;'
                        'UID=drabula;'
                        'PWD=minh03dz;'
                        'Trusted_Connection=yes;'
                        )
    print("Kết nối thành công đến cơ sở dữ liệu!")
except pyodbc.Error as ex:
    print("Lỗi kết nối đến cơ sở dữ liệu: ", ex)

query = "SELECT Temperture, Humidity, Gas, Sound, Light, TableName FROM ALLDATA"
data = pd.read_sql(query, conn)

# Tách dữ liệu thành features (đặc trưng) và labels (nhãn)
features = data[['Temperture', 'Humidity', 'Gas', 'Sound', 'Light']]
labels = data['TableName']

# Chuyển đổi dữ liệu nhãn sang dạng số
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

scaler = StandardScaler()
features = scaler.fit_transform(features)


def checkStatus(t,h,g,s,l):
    # Chuẩn bị dữ liệu mới
    new_data = pd.DataFrame([[t,h,g,s,l]], columns=['Temperture', 'Humidity', 'Gas', 'Sound', 'Light'])
    new_data = scaler.transform(new_data)
    new_data = new_data.reshape(1, 1, 1, new_data.shape[1])
    
    # Dự đoán nhãn cho dữ liệu mới
    predictions = model.predict(new_data)
    predicted_label = label_encoder.inverse_transform([np.argmax(predictions)])
    
    return predicted_label[0]
#def dataBase(t,h,g,s,l,x,d):
    cursor = conn.cursor()
    sql = "INSERT INTO DATA ([Case], Date, Temperture, Humidity, Gas, Sound, Light) VALUES ( ?, ?, ?, ?, ?, ?, ?)"
    val = (str(x),str(d), str(t), str(h), str(g), str(s), str(l))
    cursor.execute(sql, val)
    conn.commit()