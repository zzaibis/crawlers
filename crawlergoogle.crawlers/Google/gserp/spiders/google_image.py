# -*- coding: utf-8 -*-
import scrapy
import json
import scrapy
from urllib import urlencode
from w3lib.url import url_query_parameter
from gserp.items import SerpImageSearch
from gserp.gserp_db_mapping import ImageSearchParams, db


def generate_start_urls(base_url):
    start_url = []
    for serp_param in ImageSearchParams.select().where(ImageSearchParams.status == 'pending'):
        search_word = serp_param.search_word
        search_word_id = serp_param.id
        start_url.append({'url': base_url % search_word,
                         'search_word_id': search_word_id,
                          'search_word': search_word},)
    return start_url


class GoogleImageSpider(scrapy.Spider):
    name = "google_image"
    allowed_domains = ["google.com", "google.co.in"]
    # start_urls = (
    #     'https://www.google.co.in/search?q=a&tbm=isch',
    # )
    base_url = "https://www.google.com/search?tbm=isch&q=%s"

    def start_requests(self):
        for url in generate_start_urls(self.base_url):
            print url
            yield scrapy.Request(
                url=url['url'],
                callback=self.parse,
                meta={'search_word_id': url['search_word_id'],
                      'search_word': url['search_word']
                      }
            )

    def parse(self, response):
        search_word_id = response.meta['search_word_id']
        search_word = response.meta['search_word']
        # print search_word_id

        results = response.xpath(".//div[@id='rg']//div[@class='rg_meta']//text()").extract()

        if len(results) > 0:
            db.connect()
            query = ImageSearchParams.update(status='completed').where(ImageSearchParams.id == search_word_id)
            query.execute()
            db.commit()

        for result in results:
            image = json.loads(result)
            image_url = image['ou']
            image_provider = image['isu']

            item = SerpImageSearch()
            item['image_url'] = image_url
            item['image_provider'] = image_provider
            item['search_word_id'] = search_word_id
            item['search_word'] = search_word
            yield item
