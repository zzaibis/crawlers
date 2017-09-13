# __author__ = 'Dharmesh Pandav'
# Scrapy settings for dirbot project

SPIDER_MODULES = ['gserp.spiders']
NEWSPIDER_MODULE = 'gserp.spiders'

ITEM_PIPELINES = {
    # 'ad.pipelines.JsonWithEncodingPipeline': 2,
    'gserp.pipelines.GoogleMongoPipeline': 1
}

# HTTPCACHE_POLICY = "scrapy.contrib.httpcache.RFC2616Policy"
HTTPCACHE_ENABLED = False  # stored the scraped data for offline usage...
# HTTPCACHE_EXPIRATION_SECS = 0  # Set to 0 to never expire
HTTPCACHE_EXPIRATION_SECS = 86400  # This will expire after 24 hours
import random
# prevent your spider from embarrassment of being banned
DOWNLOAD_DELAY = random.randint(1,5)  # this will set random delay between 10 seconds to 30 seconds
# COOKIES_ENABLED = True

COMPRESSION_ENABLED = False

# HTTP_PROXY = 'http://54.207.49.14:80'
HTTP_PROXY = 'http://127.0.0.1:8123'

DOWNLOADER_MIDDLEWARES = {
    'gserp.middlewares.RandomUserAgentMiddleware': 400,
    'gserp.middlewares.SpiderClosingMiddleware': 401,
    #'gserp.middlewares.ProxyMiddleware': 410,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}


SPIDER_MIDDLEWARES = {
   'gserp.middlewares.CustomHttpErrorMiddleware': 543,
}

MONGO_URI = 'mongodb://104.198.195.35'
MONGO_DATABASE_GSERP = 'gserp'
MONGO_COLLECTION_GSERP = 'gserp'
MONGO_COLLECTION_GSERP_IMAGES = 'gserp'
MONGO_COLLECTION_GSERP_IMAGES_BY_WORD = 'gserp'

