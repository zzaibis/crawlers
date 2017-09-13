__author__ = 'Dharmesh Pandav'
import pymongo


class GoogleMongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db_gserp, mongo_db_collection_gserp, mongo_db_collection_gserp_images, mongo_db_collection_gserp_images_by_word):
        self.mongo_uri = mongo_uri
        self.mongo_db_gserp = mongo_db_gserp
        self.mongo_db_collection_gserp = mongo_db_collection_gserp
        self.mongo_db_collection_gserp_images = mongo_db_collection_gserp_images
        self.mongo_db_collection_gserp_images_by_word = mongo_db_collection_gserp_images_by_word

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db_gserp=crawler.settings.get('MONGO_DATABASE_GSERP'),
            mongo_db_collection_gserp=crawler.settings.get('MONGO_COLLECTION_GSERP'),
            mongo_db_collection_gserp_images=crawler.settings.get('MONGO_COLLECTION_GSERP_IMAGES'),
            mongo_db_collection_gserp_images_by_word=crawler.settings.get('MONGO_COLLECTION_GSERP_IMAGES_BY_WORD'),
        )

    def process_item(self, item, spider):
        client = pymongo.MongoClient(self.mongo_uri)
        if spider.name == "gscraper_v3":
            db = client[self.mongo_db_gserp]
            db[self.mongo_db_collection_gserp].insert(dict(item))
        elif spider.name == "gscraper_images_v3":
            db = client[self.mongo_db_gserp]
            db[self.mongo_db_collection_gserp_images].insert(dict(item))
        elif spider.name == "gscraper_images_by_word_v3":
            db = client[self.mongo_db_gserp]
            db[self.mongo_db_collection_gserp_images_by_word].insert(dict(item))

        client.close()
        return item
