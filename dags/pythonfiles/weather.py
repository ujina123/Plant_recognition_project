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

f = open("", "r", encoding="utf-8")
csv_data = csv.reader(f)

for row in csv_data:
    if (row[8]) == "\\N" and (row[9]) == "\\N":
        (row[8]) = None
        (row[9]) = None
    sql = """
            INSERT INTO weather(areaNo, si, time, condi, isDay, temp, humidity, rainRatio, snowRatio, uv)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """
    cursor.execute(sql, ((row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]) ))

conn.commit()

f.close()
conn.close()
