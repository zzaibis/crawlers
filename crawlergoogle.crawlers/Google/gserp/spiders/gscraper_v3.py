# -*- coding: utf-8 -*-
from datetime import datetime
import re
import scrapy
from w3lib.url import url_query_parameter
from gserp.helpers.string_processor import remove_white_spaces
import json
from gserp.helpers.network_manager import get_start_urls, update_search_param_status
from urllib import urlencode


def generate_start_urls(base_url,domain):
    start_url = []
    urls = json.loads(get_start_urls(domain=domain))
    for serp_param in urls:
        search_word = serp_param['search_word']
        search_word_id = serp_param['id']
        no_of_pages_per_keyword = serp_param['no_of_pages_per_keyword']
        search_param = {}
        search_group = serp_param['search_group']
        search_param['hl'] = "en"
        if serp_param['search_With_file_type']:
            search_file_type = serp_param['search_file_type']
            search_param['q'] = "filetype:%s %s" % (search_file_type, search_word)
        else:
            search_param['q'] = search_word
        start_url.append({'url': base_url + urlencode(search_param),
                          'search_word_id': search_word_id, 'search_group': search_group, 'no_of_pages_per_keyword': no_of_pages_per_keyword})
    return start_url


class GscraperSpiderV3(scrapy.Spider):
    name = "gscraper_v3"
    allowed_domains = ["google.com"]
    base_url = "https://www.google.com/search?"
    no_of_pages_per_keyword = 4
    requests_queue = []
    domain = "google"

    def start_requests(self):
        urls = generate_start_urls(self.base_url, self.domain)
        # # test Urls can be deleted later
        # urls = [
        #     # {'url':"https://www.google.com/search?q=COLUMBIA+MEMORIAL+HOSPITAL&hl=en&gws_rd=cr&ei=ou7wVsXuDoy30gSs0pXACw", 'search_word_id': "1", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "1", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "2", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "3", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "4", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "5", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "6", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "7", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "8", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "9", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "10", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "11", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "12", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "13", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "14", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "15", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "16", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "17", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "18", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "19", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "20", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "21", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "22", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "23", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "24", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "25", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "26", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "27", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "28", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "29", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "30", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "31", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "32", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "33", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "34", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "35", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "36", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "37", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "38", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "39", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "40", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "41", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "42", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "43", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "44", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "45", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "46", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "47", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "48", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "49", 'search_group': "default"},
        #     {'url':"http://httpstat.us/302", 'search_word_id': "50", 'search_group': "default"},
        # ]

        for url in urls:
            self.requests_queue.append(scrapy.Request(
                url=url['url'],
                callback=self.parse,
                meta={'search_word_id': url['search_word_id'], 'search_group': url['search_group'],
                      'dont_redirect': True, 'handle_httpstatus_list': [302], 'no_of_pages_per_keyword' : url['no_of_pages_per_keyword']},
                dont_filter=True,
            ))

        while self.requests_queue:
            yield self.requests_queue.pop()

    def parse(self, response):
        search_word_id = response.meta['search_word_id']
        no_of_pages_per_keyword = response.meta['no_of_pages_per_keyword']
        search_group = response.meta['search_group']
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
        serp_page = int(start_page) / 10 + 1 if start_page else 1
        if response.status == 200:
            update_search_param_status(search_param_id=search_word_id, domain=self.domain)
        if not response.meta.get("search_word_document"):
            search_word_document = {}
            search_word_document['search_word'] = search_word
            search_word_document['search_word_id'] = search_word_id
            search_word_document['search_file_type'] = search_file_type
            search_word_document['search_group'] = search_group
            search_word_document['Results'] = []
        else:
            search_word_document = response.meta["search_word_document"]

        search_word_page = {}
        search_word_page['search_page_no'] = serp_page
        search_word_page['page_results'] = []
        for site in sites:
            item = {}
            item['rank'] = sites.index(site) + 1
            url = site.xpath(".//h3[@class='r']/a/@href").extract_first()
            item['url'] = url
            if url and url.startswith("/url?"):
                item['url'] = url_query_parameter(response.urljoin(url), 'q')
            title = site.xpath(".//h3[@class='r']/a/text()").extract_first()
            item['title'] = remove_white_spaces(title) if title else ""
            item['short_description'] = ''.join(site.xpath(".//span[@class='st']//text()").extract())
            item['created_at'] = datetime.utcnow()
            missing_word = site.xpath(".//div[@class='_Tib']/"
                                      "span[contains(text(),'Missing')]/following-sibling::s//text()").extract()
            missing_word = ', '.join(missing_word)
            item['missing_word'] = missing_word
            search_word_page['page_results'].append(item)

        search_word_document['Results'].append(search_word_page)
        next_page = response.xpath(".//a[@id='pnnext']/@href").extract_first()
        start_index = url_query_parameter(response.url, 'start')
        start_index = int(start_index) if start_index else 0
        if next_page and start_index < (no_of_pages_per_keyword - 1) * 10:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                dont_filter=True,
                meta={'search_word_id': search_word_id,
                      'search_group': search_group,
                      'search_word_document': search_word_document,
                      'no_of_pages_per_keyword': no_of_pages_per_keyword}
            )
        else:
            yield search_word_document
