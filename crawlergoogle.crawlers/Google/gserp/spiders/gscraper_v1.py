# -*- coding: utf-8 -*-
from datetime import datetime
from pymongo import MongoClient
import re
import scrapy
from urllib import urlencode
from w3lib.url import url_query_parameter
from gserp.gserp_db_mapping import SearchParams, db
from gserp.helpers.string_processor import remove_white_spaces
from gserp.items import SerpPages


def generate_start_urls(base_url):
    start_url = []
    # SQL Input
    for serp_param in SearchParams.select().where(SearchParams.status == 'pending'):
        search_word = serp_param.search_word
        search_word_id = serp_param.id
        search_param = {}
        search_param['hl'] = "en"
        if serp_param.search_With_file_type:
            search_file_type = serp_param.search_file_type
            search_param['q'] = "filetype:%s %s" % (search_file_type, search_word)
        else:
            search_param['q'] = search_word
        start_url.append({'url': base_url + urlencode(search_param),
                         'search_word_id': search_word_id})
    return start_url


class GscraperSpiderV1(scrapy.Spider):
    name = "gscraperV1"
    allowed_domains = ["google.com"]
    base_url = "https://www.google.com/search?"
    no_of_pages_per_keyword = 2

    def start_requests(self):
        for url in generate_start_urls(self.base_url):
            print url
            yield scrapy.Request(
                url=url['url'],
                callback=self.parse,
                meta={'search_word_id': url['search_word_id']}
            )

    def parse(self, response):
        search_word_id = response.meta['search_word_id']
        sites = response.xpath("//div[@class='g']")

        query = url_query_parameter(response.url, 'q')
        start_page = url_query_parameter(response.url, 'start')

        search_file_type = re.search(r'filetype:(\w+)', query)
        search_file_type = search_file_type.group(1) if search_file_type else ""
        if search_file_type != "":
            search_word = re.search(r'filetype:\w+(.*)', query)
            search_word = search_word.group(1) if search_word else ""
        else:
            search_word = query
        serp_page = int(start_page)/10 + 1 if start_page else 1

        if len(sites) > 0:
            db.connect()
            query = SearchParams.update(status='completed').where(SearchParams.id == search_word_id)
            query.execute()
            db.commit()
        conn = MongoClient('130.211.123.250',27017)
        mdb = conn.google_res
        collection = mdb.search_res
        tmp = {}
        tmp['search_word'] =search_word
        tmp['search_word_id'] = search_word_id
        tmp['search_file_type'] = search_file_type
        tmp['search_page_no'] = serp_page
        tmp['search_url'] = response.url
        tmp['Results'] = []
        for site in sites:
            t = {}
            item = SerpPages()
            item['rank'] = sites.index(site) + 1
            t['rank'] = sites.index(site) + 1
            item['url'] = site.xpath(".//h3[@class='r']/a/@href").extract_first()
            if url.startswith("/url?"):
                item['url'] = url_query_parameter(response.urljoin(url), 'q')
            t['url'] = item['url']
            item['title'] = remove_white_spaces(str(site.xpath(".//h3[@class='r']/a/text()").extract_first()).encode('utf-8'))
            t['title'] = item['title']
            item['short_description'] = ''.join(site.xpath(".//span[@class='st']//text()").extract())
            t['short_description'] = item['short_description']
            item['created_at'] = datetime.utcnow()
            t['created_at'] = item ['created_at']
            missing_word = site.xpath(".//div[@class='_Tib']/"
                                      "span[contains(text(),'Missing')]/following-sibling::s//text()").extract()
            missing_word = ', '.join(missing_word)
            item['missing_word'] = missing_word
            t['missing_word'] = item['missing_word']
            tmp['Results'].append(t)
            #yield item
        print tmp
        collection.insert(tmp)
        next_page = response.xpath(".//a[@id='pnnext']/@href").extract_first()
        start_index = url_query_parameter(response.url,'start')
        start_index = int(start_index) if start_index else 0
        print start_index
        if next_page and start_index < (self.no_of_pages_per_keyword - 1) * 10:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                dont_filter=True,
                meta={'search_word_id': search_word_id}
            )
'''
        ad_sites = response.xpath(".//li[contains(@class,'ads-ad')]")
        for site in ad_sites:
            item = SerpPages()
            item['rank'] = ad_sites.index(site) + 1
            item['url'] = site.xpath("./h3/a[2]/@href").extract_first()
            if url.startswith("/url?"):
                item['url'] = url_query_parameter(response.urljoin(url), 'q')
            item['title'] = remove_white_spaces(''.join(site.xpath("./h3/a[2]//text()").extract()))
            item['short_description'] = ''.join(site.xpath(".//div[@class='ads-creative']//text()").extract())
            item['is_ad'] = True
            item['phone'] = ''.join(site.xpath(".//*[@class='_r2b']//text()").extract())
            item['search_word'] = search_word
            item['search_word_id'] = search_word_id
            item['search_file_type'] = search_file_type
            item['search_page_no'] = serp_page
            item['search_url'] = response.url
            item['created_at'] = datetime.utcnow()
            missing_word = site.xpath(".//div[@class='_Tib']/"
                                      "span[contains(text(),'Missing')]/following-sibling::s//text()").extract()
            missing_word = ', '.join(missing_word)
            item['missing_word'] = missing_word
            yield item
'''
