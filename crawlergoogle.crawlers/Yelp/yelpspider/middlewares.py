# __author__ = 'Dharmesh Pandav'
from scrapy.conf import settings
from yelpspider.user_agents import random_user_agent
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware, HttpError
from yelpspider.helpers.network_manager import update_search_param_status
from yelpspider.helpers.network_manager import update_search_param_status_biz
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
        if reason == "Crawler Blocked 503 Error":
            # After spider is closed for captcha error, check if any request is pending
            # pop them and update the server status back to pending
            while spider.requests_queue:
                request = spider.requests_queue.pop()
                search_param_id = request.meta['search_url_id']
                if spider.name == "yelpspider":
                    update_search_param_status(search_param_id=search_param_id, domain=spider.domain, status=0)
                if spider.name == "yelpbiz":
                    update_search_param_status_biz(search_param_id=search_param_id, domain=spider.domain, status=0)


class CustomHttpErrorMiddleware(HttpErrorMiddleware):
    def process_spider_input(self, response, spider):
        if response.status == 503:
            # First pop if any request is present in scheduler and update status back to pending on server
            for x in xrange(0, len(spider.crawler.engine.slot.scheduler)):
                request = spider.crawler.engine.slot.scheduler.mqs.pop()
                search_param_id = request.meta['search_url_id']
                if spider.name == "yelpspider":
                    update_search_param_status(search_param_id=search_param_id, domain=spider.domain, status=0)
                if spider.name == "yelpbiz":
                    update_search_param_status_biz(search_param_id=search_param_id, domain=spider.domain, status=0)

            # Then pop if any request is inprogress Queue and update status back to pending on server
            while spider.crawler.engine.slot.inprogress:
                request = spider.crawler.engine.slot.inprogress.pop()
                search_param_id = request.meta['search_url_id']
                if spider.name == "yelpspider":
                    update_search_param_status(search_param_id=search_param_id, domain=spider.domain, status=0)
                if spider.name == "yelpbiz":
                    update_search_param_status_biz(search_param_id=search_param_id, domain=spider.domain, status=0)
                # print "%s ~~~~~~~~~" % param_id
            # Need to add present request to Query else spider throws some error
            # does not create any problem still trying to keep log file clean by avoiding error logs
            spider.crawler.engine.slot.add_request(response.request)
            raise CloseSpider('Crawler Blocked 503 Error')

        return super(CustomHttpErrorMiddleware, self).process_spider_input(response, spider)

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, HttpError):
            search_param_id = response.meta['search_url_id']    
            if spider.name == "yelpspider":
                update_search_param_status(search_param_id=search_param_id, domain=spider.domain, status=3)
            if spider.name == "yelpbiz":
                update_search_param_status_biz(search_param_id=search_param_id, domain=spider.domain, status=3)

        return super(CustomHttpErrorMiddleware, self).process_spider_exception(response, exception, spider)
