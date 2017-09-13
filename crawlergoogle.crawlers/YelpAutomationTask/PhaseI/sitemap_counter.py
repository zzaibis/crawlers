
from pymongo import MongoClient
import MySQLdb, json, datetime, os
Date = datetime.datetime.now()

conn = MongoClient('mongodb://104.198.195.35:27017')

c1 = conn.yelp.yelpbiz
c2 = conn.sitemap.sitemap_count
c3 = conn.sitemap.sitemap_queue
c4 = conn.sitemap.sitemap

All_links = c1.distinct('link')
All_links.remove(None)

'''
#Initialization

for link in All_links:
    link = link.lower()
    link = link.split('/')[0]
    if len(link.split('www.')) > 1: link = link.split('www.')[1]
    link = 'http://www.' + link + '/robots.txt'
    c3.insert({'link':link, 'status':0})
    
    
Completed = c4.distinct('website')
for link in Completed:
    link = link.lower()
    link = link.split('/')[0]
    if len(link.split('www.')) > 1: link = link.split('www.')[1]
    link = 'http://www.' + link + '/robots.txt'
    c3.update({'link':link},{'$set':{'status':1}})
'''

if len(All_links) == int(c2.find_one()['count']):
    exit()
else:
    delta = len(All_links) - int(c2.find_one()['count'])
    Data = c1.find(no_cursor_timeout = True).sort('_id',-1).limit(delta)
    for data in Data:
        link = data['link']
        link = link.lower()
        link = link.split('/')[0]
        if len(link.split('www.')) > 1: link = link.split('www.')[1]
        link = 'http://www.' + link + '/robots.txt'
        if c3.find({'link':link}).count() == 0:
            c3.insert({'link':link,'status':0})
            c2.update({},{'$set':{'count':len(All_links)}})
