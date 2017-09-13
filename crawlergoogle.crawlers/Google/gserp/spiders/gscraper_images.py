# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from gserp.helpers.string_processor import remove_white_spaces
from gserp.items import SerpImagePages
from w3lib.url import url_query_parameter
from gserp.gserp_db_mapping import SearchImageParams, db


def generate_start_urls(base_url,base_ip):
    start_url = []
    for serp_param in SearchImageParams.select().where(SearchImageParams.status == 'pending'):
        search_image_name = serp_param.search_image_name
        search_image_id = serp_param.id
        search_image_url = serp_param.search_image_url
        start_url.append({'url': base_url % (base_ip, search_image_url),
                         'search_image_id': search_image_id,
                          'search_image_name': search_image_name})
    return start_url


class GscraperImagesSpider(scrapy.Spider):
    name = "gscraper_images"
    allowed_domains = ["google.com"]
    # start_urls = (
    #     'https://images.google.com/searchbyimage?image_url=http://104.197.118.137/image/bulb-1239423_960_720.jpg&encoded_image=&image_content=&filename=&hl=en',
    # )
    base_ip = "http://104.197.118.137"
    no_of_pages_per_keyword = 4
    base_url = 'https://images.google.com/searchbyimage?' \
        'image_url=%s/%s' \
        '&encoded_image=' \
        '&image_content=' \
        '&filename=' \
        '&hl=en'

    def start_requests(self):

        for url in generate_start_urls(self.base_url, self.base_ip):
            print url
            yield scrapy.Request(
                url=url['url'],
                callback=self.parse,
                dont_filter=True,
                meta={'search_image_id': url['search_image_id'],
                      'search_image_name': url['search_image_name']}
            )

    def parse(self, response):
        search_image_name = response.meta['search_image_name']
        search_image_id = response.meta['search_image_id']
        start_page = url_query_parameter(response.url, 'start')
        serp_page = int(start_page)/10 + 1 if start_page else 1
        sites = response.xpath('//div[@class="srg"]/div[@class="g"]')
        if len(sites) > 0:
            db.connect()
            q = SearchImageParams.update(status='completed').where(SearchImageParams.id == search_image_id)
            q.execute()
            db.commit()

        for site in sites:
            rank = sites.index(site) + 1
            url = site.xpath(".//h3[@class='r']/a/@href").extract_first()
            title = remove_white_spaces(site.xpath(".//h3[@class='r']/a/text()").extract_first())
            image_url = response.urljoin(site.xpath(".//div[@class='th _lyb']/a/@href").extract_first())
            image_url = url_query_parameter(image_url, 'imgurl')
            short_description = ''.join(site.xpath(".//span[@class='st']//text()").extract())
            search_url = response.url
            created_at = datetime.utcnow()

            item = SerpImagePages()
            item['rank'] = rank
            item['url'] = url
            item['title'] = title
            item['image_url'] = image_url
            item['short_description'] = short_description
            item['search_image_id'] = search_image_id
            item['search_image_name'] = search_image_name
            item['search_page_no'] = serp_page
            item['search_url'] = search_url
            item['created_at'] = created_at
            yield item

        next_page = response.xpath(".//a[@id='pnnext']/@href").extract_first()
        start_index = url_query_parameter(response.url,'start')
        start_index = int(start_index) if start_index else None
        if next_page and start_index < (self.no_of_pages_per_keyword - 1) * 10:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                dont_filter=True,
                meta={'search_image_id': search_image_id,
                      'search_image_name': search_image_name}
            )
