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
    sql = """
            INSERT INTO plantdisease
            VALUES (%s, %s, %s, %s, %s, %s)
          """
    cursor.execute(sql, ( (row[0]), (row[1]), (row[2]), (row[3]), (row[4]), (row[5]) ))

conn.commit()

f.close()
conn.close()
