# __author__ = 'Dharmesh Pandav'
from scrapy.conf import settings
from gserp.user_agents import random_user_agent
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware, HttpError
from gserp.helpers.network_manager import update_search_param_status
from scrapy.exceptions import CloseSpider
from scrapy import signals

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random_user_agent()
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')


class SpiderClosingMiddleware(object):
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_closed, signal=signals.stats_spider_closed)
        return o

    @classmethod
    def spider_closed(cls, spider, reason):

        if reason == "Crawler Blocked 302 captcha error":
            # After spider is closed for captcha error, check if any request is pending
            # pop them and update the server status back to pending
            while spider.requests_queue:
                request = spider.requests_queue.pop()
                if spider.name == 'gscraper_images':
                    param_id = request.meta['search_image_id']
                elif spider.name == 'gscraper_images_by_word':
                    param_id = request.meta['image_search_word_id']
                else:
                    param_id = request.meta['search_word_id']
                update_search_param_status(search_param_id=param_id, domain=spider.domain, status=0)
                # print "%s ^^^^^^^^^^^^^" % param_id


class CustomHttpErrorMiddleware(HttpErrorMiddleware):
    def process_spider_input(self, response, spider):
        if response.status == 302:
            # First pop if any request is present in scheduler and update status back to pending on server
            for x in xrange(0, len(spider.crawler.engine.slot.scheduler)):
                request = spider.crawler.engine.slot.scheduler.mqs.pop()
                if spider.name == 'gscraper_images':
                    param_id = request.meta['search_image_id']
                elif spider.name == 'gscraper_images_by_word':
                    param_id = response.meta['image_search_word_id']
                else:
                    param_id = request.meta['search_word_id']
                update_search_param_status(search_param_id=param_id, domain=spider.domain, status=0)

            # Then pop if any request is inprogress Queue and update status back to pending on server
            while spider.crawler.engine.slot.inprogress:
                request = spider.crawler.engine.slot.inprogress.pop()
                if spider.name == 'gscraper_images':
                    param_id = request.meta['search_image_id']
                elif spider.name == 'gscraper_images_by_word':
                    param_id = response.meta['image_search_word_id']
                else:
                    param_id = request.meta['search_word_id']
                update_search_param_status(search_param_id=param_id, domain=spider.domain, status=0)
                # print "%s ~~~~~~~~~" % param_id
            # Need to add present request to Query else spider throws some error
            # does not create any problem still trying to keep log file clean by avoiding error logs
            spider.crawler.engine.slot.add_request(response.request)
            raise CloseSpider('Crawler Blocked 302 captcha error')

        return super(CustomHttpErrorMiddleware, self).process_spider_input(response, spider)

    def process_spider_exception(self, response, exception, spider):
        if spider.name == 'gscraper_images':
            param_id = response.meta['search_image_id']
        elif spider.name == 'gscraper_images_by_word':
            param_id = response.meta['image_search_word_id']
        else:
            param_id = response.meta['search_word_id']

        if isinstance(exception, HttpError):
            update_search_param_status(search_param_id=param_id, domain=spider.domain, status=3)
            # print "%s ###########" % param_id

        # http://stackoverflow.com/questions/28169756/how-to-get-the-number-of-requests-in-queue-in-scrapy

        return super(CustomHttpErrorMiddleware, self).process_spider_exception(response, exception, spider)
