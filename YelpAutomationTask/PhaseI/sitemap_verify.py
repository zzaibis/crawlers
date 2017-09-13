from pymongo import MongoClient

conn = MongoClient('mongodb://104.198.195.35:27017')
db = conn.sitemap
c1 = db.sitemap
c2 = db.sitemap_queue

twos = c2.find({'status':2}, no_cursor_timeout = True)

for two in twos:
    website = two['link'].split('/robots')[0]
    website = website.split('http://www.')[1]
    #print website
    try:
        if len(c1.find_one({'website':website})) > 0:
            c2.update({'_id':two['_id']},{'$set':{'status':1}}, multi = True)
    except:
        c2.update({'_id':two['_id']},{'$set':{'status':3}})
