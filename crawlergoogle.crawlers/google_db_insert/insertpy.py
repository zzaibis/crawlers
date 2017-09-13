import glob
import os
import csv
import MySQLdb, datetime, csv
#os.chdir("Incomplete")

Date = datetime.datetime.now()

db = MySQLdb.connect("localhost","root","zaibis1991","crawler")



glob_files = glob.glob("*.csv")
#print glob_files

files = []
for file in glob_files:
        files.append(file)
#print files

cursor = db.cursor()

search_data = []
for obj in files:
    #print obj
    with open(obj) as f:
        data = csv.DictReader(f)
        part_one = []
        part_two = []
        for row in data:
                #print row
                print (row['word2'])
                part_one.append(row['word1'])
                part_two.append(row['word2'])
        for one in part_one:
            for two in part_two:
                new_word = one + " " + two
                search_data.append(new_word)

sql_create = "CREATE TABLE google3 (search_word VARCHAR(64) NOT NULL,status INT NOT NULL,priority INT NULL,search_group VARCHAR(64) NOT NULL,slave_server_ip VARCHAR(64) NOT NULL,created_at date NOT NULL)"
try:
	cursor.execute(sql_create)
except:
	pass
for obj in search_data:
    print('2____________________')                
    print (obj)
    print('2____________________')                
    sql = """INSERT INTO google3  (search_word,status,priority,search_group,slave_server_ip,created_at) VALUES (%s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(sql, (obj, "0","1", "group", "0", Date.strftime("%Y-%m-%d")))
       	db.commit()
    except:
        print ("Hold the door")
        db.rollback()
            
db.close()

#for file in glob_files:
#    os.rename("/home/zzaibis/Incomplete/"+file,"/home/zzaibis/Complete/"+file)
    
    
#insert into searchparams (search_word,status,priority,search_group,slave_server_ip,created_at)
