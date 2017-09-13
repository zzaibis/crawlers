# __author__ = 'Dharmesh Pandav'
import pymongo


class SitemapMongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db_sitemap, mongo_db_collection_sitemap):
        self.mongo_uri = mongo_uri
        self.mongo_db_sitemap = mongo_db_sitemap
        self.mongo_db_collection_sitemap = mongo_db_collection_sitemap

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db_sitemap=crawler.settings.get('MONGO_DATABASE_SITEMAP'),
            mongo_db_collection_sitemap=crawler.settings.get('MONGO_COLLECTION_SITEMAP'),
        )

    def process_item(self, item, spider):
        client = pymongo.MongoClient(self.mongo_uri)
        if spider.name == "sitemapspider":
            db = client[self.mongo_db_sitemap]
            # db[self.mongo_db_collection_sitemap].insert(dict(item))
            db[self.mongo_db_collection_sitemap].insert_many([dict(x) for x in item['source']])
        client.close()
        return item
