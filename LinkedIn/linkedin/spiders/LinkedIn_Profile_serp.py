# -*- coding: utf-8 -*-
import re
import json
from urllib import urlencode
from operator import itemgetter
from scrapy.spiders import Spider, Request

from linkedin.helpers.network_manager import get_start_urls, update_search_param_status


def generate_start_urls(base_url, domain):
    start_url = []
    urls = json.loads(get_start_urls(domain=domain))
    for serp_param in urls:
        search_word_id = serp_param['id']
        no_of_pages_per_keyword = serp_param['no_of_pages_per_keyword']
        search_group = serp_param['search_group']

        search_param = {}
        search_word = "%s %s %s" % (serp_param['word1'], serp_param['word2'], serp_param['word3'])
        search_param['q'] = "site:linkedin.com %s" + search_word
        start_url.append({'url': base_url + urlencode(search_param),
                          'search_word_id': search_word_id,
                          'search_group': search_group,
                          'no_of_pages_per_keyword': no_of_pages_per_keyword,
                          'word1': serp_param['word1'],
                          'word2': serp_param['word2'],
                          'word3': serp_param['word3'],
                          'search_word': search_word})
    # search_param = {}
    # search_param['q'] = "site:linkedin.com " + "premier logic llc"
    # start_url.append({'url': base_url + urlencode(search_param),
    #                   'search_word_id': 1,
    #                   'search_group': "deafault",
    #                   'no_of_pages_per_keyword': 1,
    #                   'word1': "premier",
    #                   'word2': "logic",
    #                   'word3': "llc",
    #                   'search_word': "premier logic llc"})
    return start_url


class BingSearchLinkedIn(Spider):
    name = 'bing_serp_linkedin'
    domain = 'linked_in_bing'
    allowed_domains = ['www.bing.com']
    start_urls = ["https://www.bing.com"]
    word1_count = 0
    word2_count = 0
    word3_count = 0
    counter = 0
    base_url = "https://www.bing.com/search?"
    requests_queue = []
    custom_settings = {
        "DOWNLOAD_DELAY": 0
    }

    def start_requests(self):
        urls = generate_start_urls(self.base_url, self.domain)
        for url in urls:
            self.requests_queue.append(Request(
                url=url['url'],
                callback=self.parse,
                meta={'search_word_id': url['search_word_id'],
                      'search_group': url['search_group'],
                      'dont_redirect': True,
                      'handle_httpstatus_list': [302],
                      'no_of_pages_per_keyword': url['no_of_pages_per_keyword'],
                      'word1': url['word1'],
                      'word2': url['word2'],
                      'word3': url['word3'],
                      'search_word': url['search_word']
                      },
                dont_filter=True,
            ))

        while self.requests_queue:
            yield self.requests_queue.pop()

    def parse(self, response):

        self.counter = 0
        word1 = response.meta['word1'].lower()
        word2 = response.meta['word2'].lower()
        word3 = response.meta['word3'].lower()
        word3 = re.split("[. |]", word3)[0]

        search_word = response.meta['search_word'].lower()
        search_word_id = response.meta['search_word_id']
        search_group = response.meta['search_group']
        no_of_pages_per_keyword = response.meta['no_of_pages_per_keyword']

        if response.status == 200:
            update_search_param_status(search_param_id=search_word_id, domain=self.domain)

        search_word_document = {}
        search_word_document['search_word'] = search_word
        search_word_document['word1'] = word1
        search_word_document['word2'] = word2
        search_word_document['word3'] = word3
        search_word_document['search_word_id'] = search_word_id
        search_word_document['search_group'] = search_group
        search_word_document['Results'] = []

        sites = response.xpath("//li[@class='b_algo']")
        for i, site in enumerate(sites):
            item = {}
            website_url = ''.join(site.xpath('.//div[@class="b_attribution"]//text()').extract())
            # website_url = urljoin("http://linkedin.com/", website_url)
            text = ''.join(site.xpath('.//div[@class="b_caption"]//text()').extract()).lower()
            self.word1_count = text.count(word1) if word1 else 0
            self.word2_count = text.count(word2) if word2 else 0
            self.word3_count = text.count(word3) if word3 else 0
            total = self.word1_count + self.word2_count + self.word3_count
            item["word1_count"] = self.word1_count
            item["word2_count"] = self.word2_count
            item["word3_count"] = self.word3_count
            item["total"] = total
            item["search_word_id"] = search_word_id
            item["url_linkedin"] = website_url
            item["url_bing"] = response.url
            item["index"] = i
            item["search_words"] = "%s|%s|%s" % (word1 or "-", word2 or "-", word3 or "-")
            if '/in/' in website_url:
                item['record_type'] = "individual"
            elif '/pub/' in website_url:
                item['record_type'] = "directory"
            elif '/company/' in website_url and '/companies/' in website_url:
                item['record_type'] = "company"
            elif '/jobs/' in website_url or '/jobs2/' in website_url:
                item['record_type'] = "jobs"
            elif '/pulse/' in website_url:
                item['record_type'] = "pulse"
            else:
                item['record_type'] = "general"
            # yield item
            search_word_document['Results'].append(item)

        # sort result from highest to lowest count
        search_word_document['Results'] = sorted(search_word_document['Results'], key=itemgetter('total'), reverse=True)
        yield search_word_document
        # full_match = False
        # for result in search_result:
        #     if result['fname_count'] != 0 and result['lname_count'] != 0 and result['company_count'] != 0:
        #         yield result
        #         full_match = True
        #     elif result['total'] > 2 and (result['fname_count'] != 0 and result['lname_count'] != 0) and full_match == False:
        #         yield result
