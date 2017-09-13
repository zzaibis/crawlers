import glob
import os
import csv
import MySQLdb, datetime, csv
#os.chdir("Incomplete")

Date = datetime.datetime.now()

db = MySQLdb.connect("localhost","root","zaibis1991","crawler")


cursor = db.cursor()



search_data = ['zaibi','noorain', 'naukhaiz', 'mom','dad', 'padosi']

#sql = "CREATE TABLE googlesearch"

#cursor.execute(sql)

for obj in search_data:
    sql = "INSERT INTO googlesearch (search_word,status,priority,search_group,slave_server_ip,created_at) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (obj, "0","1", "group", "0", Date.strftime("%Y-%m-%d")))
    db.commit()

    try:
        cursor.execute(sql, (obj, "0","1", "group", "0", Date.strftime("%Y-%m-%d")))
       	db.commit()
    except:
        print ("Hold the door")
        db.rollback()
            
db.close()
