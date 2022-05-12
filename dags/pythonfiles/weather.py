# JngMkk
import pymysql
import csv

conn = pymysql.connect(
    user="root",
    passwd="1234",
    host="localhost",
    db="finalproject",
    charset="utf8"
)

cursor = conn.cursor()

f = open("/home/jngmk/weather.csv", "r", encoding="utf-8")
csv_data = csv.reader(f)

for row in csv_data:
    if (row[8]) == "\\N":
        (row[8]) = None
    if (row[9]) == "\\N":
        (row[9]) = None
    if (row[10]) == "\\N":
        (row[10]) = None
    sql = """
            INSERT INTO weather(areaNo, si, time, condi, isDay, temp, humidity, humidInfo, rainRatio, snowRatio, uv, uvInfo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """
    cursor.execute(sql, ((row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]) ))

conn.commit()

f.close()
conn.close()
