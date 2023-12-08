import pyodbc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam


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

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Reshape dữ liệu để phù hợp với mô hình CNN
#1d sang 4d (so luong mau,chieucao,chiuẻong,sokenh)
X_train = X_train.reshape(X_train.shape[0], 1, 1, X_train.shape[1])
X_test = X_test.reshape(X_test.shape[0], 1, 1, X_test.shape[1])

model = Sequential()
model.add(Conv2D(64, (1, 1), activation='relu', input_shape=(1, 1, X_train.shape[3])))
model.add(MaxPooling2D((1, 1)))
model.add(Conv2D(128, (1, 1), activation='relu'))
model.add(MaxPooling2D((1, 1)))
model.add(Conv2D(256, (1, 1), activation='relu'))
model.add(MaxPooling2D((1, 1)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(len(label_encoder.classes_), activation='softmax'))

# Biên dịch mô hình
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=100, batch_size=16, validation_data=(X_test, y_test))
loss, accuracy = model.evaluate(X_test, y_test)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)
np.save('label_encoder.npy', label_encoder.classes_)
# Lưu mô hình đã huấn luyện
model.save('my_model.keras')
model.save_weights('my_weights.keras')
print("Mô hình đã được lưu.")