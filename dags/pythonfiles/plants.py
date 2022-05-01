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

f = open("경로", "r", encoding="utf-8")
csv_data = csv.reader(f)

for row in csv_data:
    sql = """
            INSERT INTO plants
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """
    cursor.execute(sql, ((row[0]), (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17])))

conn.commit()

f.close()
conn.close()
