import logging

from scrapy.spiders import SitemapSpider
from scrapy.http import Request
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
import tldextract
from ..helpers.string_processor import deduplicate_list


logger = logging.getLogger(__name__)

# dependencies : need to install mongo cache middleware 
# https://github.com/scrapinghub/scmongo.git
# python setup.py install

# Best practice would be
# we feed in domain name
# based on that following url's will be tried:
# 1. example.com/robots.txt - this one is implemented
# 2. example.com/sitemap.xml - this one is implemented
# 3. example.com and collect all href from the page


class SitemapspiderSpider(SitemapSpider):
    name = "sitemapspider"
    sitemap_urls = (
        # "http://www.bromwichhardy.com/sitemap.xml",
        # "http://www.511tactical.com/robots.txt",
        # "http://www.amazon.in/robots.txt",  # amazon is bad example , compatibility issue with scrapy
        "http://www.amazon.in",
    )

    def _parse_sitemap(self, response):
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.body):
                yield Request(url, callback=self._parse_sitemap)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                extracted = tldextract.extract(response.url)
                website = "{}.{}".format(extracted.domain, extracted.suffix)
                all_links = response.xpath(".//a/@href").extract()
                all_links = [response.urljoin(link) for link in all_links if link and "#" not in link]
                all_links = deduplicate_list(all_links)
                items = {}
                items['source'] = []
                for link in all_links:
                    item = {'website': website, 'url': link, 'source': "website"}
                    items['source'].append(item)
                yield items
                # logger.warning("Ignoring invalid sitemap: %(response)s",
                #                {'response': response}, extra={'spider': self})
                return

            s = Sitemap(body)
            if s.type == 'sitemapindex':
                for loc in iterloc(s, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == 'urlset':
                extracted = tldextract.extract(response.url)
                website = "{}.{}".format(extracted.domain, extracted.suffix)
                items = {}
                items['source'] = []
                for loc in iterloc(s):
                    for r, c in self._cbs:

                        if r.search(loc):
                            item = {'website': website, 'url': loc, 'source': "xml"}
                            items['source'].append(item)
                            # yield item
                            break
                yield items



    # def parse(self, response):
    #     url = response.url
    #     item = Tactical511Item()
    #     item['url'] = url
    #     # print response.url
    #     yield item


def iterloc(it, alt=False):
    for d in it:
        yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                yield l
