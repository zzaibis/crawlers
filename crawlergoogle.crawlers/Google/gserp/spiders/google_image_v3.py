# -*- coding: utf-8 -*-
import scrapy
from urllib import urlencode
from w3lib.url import url_query_parameter
from gserp.helpers.network_manager import get_start_urls, update_search_param_status
import json


def generate_start_urls(base_url, domain):
    start_url = []
    urls = json.loads(get_start_urls(domain=domain))
    for serp_param in urls:
        image_search_word = serp_param.image_search_word
        image_search_word_id = serp_param.id
        start_url.append({'url': base_url % image_search_word,
                         'image_search_word_id': image_search_word_id,
                          'image_search_word': image_search_word,
                          'search_group': serp_param.search_group,
                          'no_of_pages_per_keyword': serp_param.no_of_pages_per_keyword
                          },)
    return start_url


class GoogleImageSpiderV3(scrapy.Spider):
    name = "gscraper_images_by_word_v3"
    domain = "gimagesbyword"
    allowed_domains = ["google.com", "google.co.in"]
    # start_urls = (
    #     'https://www.google.co.in/search?q=a&tbm=isch',
    # )
    base_url = "https://www.google.com/search?tbm=isch&q=%s"
    requests_queue = []

    def start_requests(self):
        urls = generate_start_urls(self.base_url, self.domain)
        for url in urls:
            self.requests_queue.append(scrapy.Request(
                url=url['url'],
                callback=self.parse,
                meta={'image_search_word_id': url['image_search_word_id'],
                      'image_search_word': url['image_search_word'],
                      'search_group': url['search_group'],
                      'no_of_pages_per_keyword': url['no_of_pages_per_keyword']
                      }
            ))

        while self.requests_queue:
            yield self.requests_queue.pop()

    def parse(self, response):
        image_search_word_id = response.meta['image_search_word_id']
        image_search_word = response.meta['image_search_word']
        search_group = response.meta['search_group']
        # no_of_pages_per_keyword = response.meta['no_of_pages_per_keyword']
        # start_page = url_query_parameter(response.url, 'start')
        # serp_page = int(start_page) / 10 + 1 if start_page else 1

        results = response.xpath(".//div[@id='rg']//div[@class='rg_meta']//text()").extract()

        if response.status == 200:
            update_search_param_status(search_param_id=image_search_word_id, domain=self.domain, status=2)

        if not response.meta.get("search_image_document"):
            image_search_word_document = {}
            image_search_word_document['image_search_word'] = image_search_word
            image_search_word_document['image_search_word_id'] = image_search_word_id
            image_search_word_document['search_group'] = search_group
            image_search_word_document['Results'] = []
        else:
            image_search_word_document = response.meta["image_search_word_document"]

        image_search_word_page = {}
        image_search_word_page['search_page_no'] = "1"
        image_search_word_page['page_results'] = []
        for result in results:
            image = json.loads(result)
            image_url = image['ou']
            image_provider = image['isu']

            item = {}
            item['image_url'] = image_url
            item['image_provider'] = image_provider
            image_search_word_page['page_results'].append(item)

        image_search_word_document['Results'].append(image_search_word_page)

        yield image_search_word_document
