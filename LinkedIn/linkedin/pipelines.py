# __author__ = 'Dharmesh Pandav'
import pymongo


class LinkedinPipeline(object):

    def __init__(self, mongo_uri, mongo_db_linked_individual, mongo_db_collection_linked_individual,
                 mongo_db_linked_company, mongo_db_collection_linked_company,
                 mongo_db_bing_serp_linkedin, mongo_db_collection_bing_serp_linkedin):
        self.mongo_uri = mongo_uri
        self.mongo_db_linked_individual = mongo_db_linked_individual
        self.mongo_db_collection_linked_individual = mongo_db_collection_linked_individual
        self.mongo_db_linked_company = mongo_db_linked_company
        self.mongo_db_collection_linked_company = mongo_db_collection_linked_company
        self.mongo_db_bing_serp_linkedin = mongo_db_bing_serp_linkedin
        self.mongo_db_collection_bing_serp_linkedin = mongo_db_collection_bing_serp_linkedin

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db_linked_individual=crawler.settings.get('MONGO_DATABASE_LINKEDIN_INDIVIDUAL'),
            mongo_db_collection_linked_individual=crawler.settings.get('MONGO_COLLECTION_LINKEDIN_INDIVIDUAL'),
            mongo_db_linked_company=crawler.settings.get('MONGO_DATABASE_LINKEDIN_COMPANY'),
            mongo_db_collection_linked_company=crawler.settings.get('MONGO_COLLECTION_LINKEDIN_COMPANY'),
            mongo_db_bing_serp_linkedin=crawler.settings.get('MONGO_DATABASE_BING_SERP_LINKEDIN'),
            mongo_db_collection_bing_serp_linkedin=crawler.settings.get('MONGO_COLLECTION_BING_SERP_LINKEDIN'),
        )

    def process_item(self, item, spider):
        client = pymongo.MongoClient(self.mongo_uri)
        if spider.name == "bing_serp_linkedin":
            db = client[self.mongo_db_bing_serp_linkedin]
            db[self.mongo_db_collection_bing_serp_linkedin].insert(dict(item))
        elif spider.name == "linkedin_person_profile":
            db = client[self.mongo_db_linked_individual]
            db[self.mongo_db_collection_linked_individual].insert(dict(item))
        elif spider.name == "linkedin_company_profile":
            db = client[self.mongo_db_linked_company]
            db[self.mongo_db_collection_linked_company].insert(dict(item))
        client.close()
        return item
