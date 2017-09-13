# __author__ = 'jonsnow'
from gserp.gserp_db_mapping import SearchResult, SearchParams
import MySQLdb

db1 = MySQLdb.connect(host="localhost", user="root", passwd="gghhjj1")
cursor = db1.cursor()
sql = 'CREATE DATABASE gserp DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;'
cursor.execute(sql)
db1.close()
SearchParams.create_table()
SearchResult.create_table()

