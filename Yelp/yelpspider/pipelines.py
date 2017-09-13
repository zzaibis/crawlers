# __author__ = 'Dharmesh Pandav'
import pymongo


class YelpMongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db_yelp, mongo_db_collection_yelp, mongo_db_collection_yelp_biz):
        self.mongo_uri = mongo_uri
        self.mongo_db_yelp = mongo_db_yelp
        self.mongo_db_collection_yelp = mongo_db_collection_yelp
        self.mongo_db_collection_yelp_biz = mongo_db_collection_yelp_biz

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db_yelp=crawler.settings.get('MONGO_DATABASE_YELP'),
            mongo_db_collection_yelp=crawler.settings.get('MONGO_COLLECTION_YELP'),
            mongo_db_collection_yelp_biz=crawler.settings.get('MONGO_COLLECTION_YELP_BIZ')
            
        )

    def process_item(self, item, spider):
        client = pymongo.MongoClient(self.mongo_uri)
        if spider.name == "yelpspider":
            db = client[self.mongo_db_yelp]
            db[self.mongo_db_collection_yelp].insert(dict(item))
        if spider.name == "yelpbiz":
            db = client[self.mongo_db_yelp]
            db[self.mongo_db_collection_yelp_biz].insert(dict(item))
        client.close()
        return item
        
