# __author__ = 'Dharmesh Pandav'
from sitemap_spider.user_agents import random_user_agent


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random_user_agent()
        if ua:
            request.headers.setdefault('User-Agent', ua)

