BOT_NAME = 'linkedin'

SPIDER_MODULES = ['linkedin.spiders']
NEWSPIDER_MODULE = 'linkedin.spiders'
#CONCURRENT_REQUESTS=32
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

#COOKIES_ENABLED=False

SPIDER_MIDDLEWARES = {
   'linkedin.middlewares.CustomHttpErrorMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'linkedin.middlewares.RandomUserAgentMiddleware': 400,
    'linkedin.middlewares.SpiderClosingMiddleware': 401,
    #'linkedin.middlewares.ProxyMiddleware': 410,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
ITEM_PIPELINES = {
   'linkedin.pipelines.LinkedinPipeline': 300,
}

# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 20
# AUTOTHROTTLE_MAX_DELAY = 60

#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOAD_DELAY = 20  # this will set random delay between 10 seconds to 30 seconds
# COOKIES_ENABLED = True
# COMPRESSION_ENABLED = False

HTTP_PROXY = 'http://127.0.0.1:8123'


MONGO_URI = 'mongodb://104.197.3.87'

MONGO_DATABASE_LINKEDIN_INDIVIDUAL = 'linkedin_individual'
MONGO_COLLECTION_LINKEDIN_INDIVIDUAL = 'linkedin_individual'

MONGO_DATABASE_LINKEDIN_COMPANY = 'linkedin_company'
MONGO_COLLECTION_LINKEDIN_COMPANY = 'linkedin_company'

MONGO_DATABASE_BING_SERP_LINKEDIN = 'bing_serp_linkedin'
MONGO_COLLECTION_BING_SERP_LINKEDIN = 'bing_serp_linkedin'
