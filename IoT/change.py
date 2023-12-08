import pyodbc
import random
from decimal import Decimal, ROUND_HALF_UP

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

# Tạo con trỏ
cursor = conn.cursor()

# Lấy dữ liệu từ cơ sở dữ liệu
cursor.execute("SELECT ID FROM IoT_7")
rows = cursor.fetchall()

# Cập nhật giá trị nhiệt độ ngẫu nhiên cho mỗi dòng
for row in rows:
    temperature = Decimal(random.uniform(20, 30)).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
    cursor.execute("UPDATE IoT_7 SET Temperture = ? WHERE ID = ?", (temperature, row[0]))

# Lưu các thay đổi vào cơ sở dữ liệu
conn.commit()

# Đóng kết nối
conn.close()