#This script is meant to be executed every 5 minutes via cron

from pymongo import MongoClient
import MySQLdb, json, datetime, os
Date = datetime.datetime.now()

conn = MongoClient('mongodb://104.198.195.35:27017')
db = conn.yelp
counter = db.insert_count
collection = db.yelp
collection_biz = db.yelpbiz


mysqldb = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="gghhjj1", db="crawler")
cursor = mysqldb.cursor()


def biz_insert(url):
    #mysqldb = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="gghhjj1", db="crawler")
    #cursor = mysqldb.cursor()
    sql = "INSERT INTO yelpbizparams (search_url, status, priority, search_group, created_at) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (url, "0", "1", str(Date), Date.strftime("%Y-%m-%d")))
        mysqldb.commit()
    except:
        print "WTF"
        db.rollback()
    #mysqldb.close()



if int(collection.find().count()) == int(counter.find_one()['count']):
    exit()
else:
    #Insert New Records
    delta = int(collection.find().count()) - int(counter.find_one()['count'])
    Data = collection.find(no_cursor_timeout = True).sort('_id',-1).limit(delta)
    for data in Data:
        for dat  in data['Results']:
            for da in dat['page_results']:
                url = da['url'].split('?search_key')[0]
                if not collection_biz.find({'yelp_url' : url}).count() > 0:
                    biz_insert(url)
    counter.update({},{'$set' : {'count' : int(collection.find().count())}})
    mysqldb.close()
