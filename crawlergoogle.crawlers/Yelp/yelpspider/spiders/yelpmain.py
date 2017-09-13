# -*- coding: utf-8 -*-
import re
import scrapy
from w3lib.url import url_query_parameter
import json
from yelpspider.helpers.network_manager import get_start_urls, update_search_param_status
from yelpspider.helpers.string_processor import join_address_elements, remove_white_spaces


def generate_start_urls(domain):
    start_url = []
    urls = json.loads(get_start_urls(domain=domain))
    for url in urls:
        start_url.append({'url': url['search_url'],
                          'search_url_id': url['id'],
                          'search_group': url['search_group'],
                          'visit_details_page': url['visit_details_page'],
                          'no_of_pages_to_visit': url['no_of_pages_to_visit']})
    return start_url


class YelpmainSpider(scrapy.Spider):
    handle_httpstatus_list = [500, 502,503]
    name = "yelpspider"
    domain = "yelp"
    allowed_domains = ["www.yelp.com"]
    start_urls = (
        'http://www.yelp.com/search?cflt=gyms&find_loc=Upper East Side%2C Manhattan%2C NY',
    )
    requests_queue = []

    def start_requests(self):
        urls = generate_start_urls(self.domain)
        for url in urls:
            self.requests_queue.append(scrapy.Request(
                url=url['url'],
                callback = self.parse,
                meta={
                    'visit_details_page': url['visit_details_page'],
                    'search_url_id': url['search_url_id'],
                    'no_of_pages_to_visit': url['no_of_pages_to_visit'],
                    'search_group': url['search_group'],
                    'search_url': url['url'],
                    'serp_page': '1',
                    'handle_httpstatus_list': [503]
                },
                dont_filter=True
            ))

        while self.requests_queue:
            yield self.requests_queue.pop()


    def parse(self, response):
        # print "visit_details_page %s" % response.meta['visit_details_page']
        # print "no_of_pages_to_visit %s" % response.meta['no_of_pages_to_visit']
        visit_details_page = response.meta['visit_details_page']
        search_url = response.meta['search_url']
        search_url_id = response.meta['search_url_id']
        search_group = response.meta['search_group']
        no_of_pages_to_visit = response.meta['no_of_pages_to_visit']
        product_listing = response.xpath('//div[contains(@class, "natural-search-result")]')
        # print len(product_listing)
        search_string = ', '.join(response.xpath('.//div[contains(@class,"search-header")]//h1//text()').extract())
        search_string = remove_white_spaces(search_string)

        if len(product_listing) > 0:
            update_search_param_status(search_param_id=search_url_id, domain=self.domain,status=2)

        if not response.meta.get("search_url_document"):
            search_url_document = {}
            search_url_document['search_url'] = search_url
            search_url_document['search_string'] = search_string
            search_url_document['search_url_id'] = search_url_id
            search_url_document['search_group'] = search_group
            search_url_document['Results'] = []
            serp_page = 1
        else:
            search_url_document = response.meta["search_url_document"]
            serp_page = int(response.meta['serp_page'])

        search_url_page = {}
        search_url_page['search_page_no'] = serp_page
        search_url_page['page_results'] = []

        for product in product_listing:
            rank = product.xpath("@data-key").extract_first()
            url = product.xpath(".//a[@data-analytics-label='biz-name']/@href").extract_first()
            url = response.urljoin(url) if url else ""
            name = ''.join(product.xpath(".//a[@data-analytics-label='biz-name']//text()").extract())
            rating = product.xpath(".//div[@class='rating-large']//i//@title").extract_first()
            rating = re.search(r'[\d\.]+', rating).group(0) if rating else ""
            no_of_reviews = ''.join(product.xpath(".//span[contains(@class,'review-count')]//text()").extract())
            no_of_reviews = re.search(r'\d+', no_of_reviews).group(0) if no_of_reviews else '0'
            tags = ', '.join(product.xpath(".//span[@class='category-str-list']//a//text()").extract())
            address_street = product.xpath(".//span[@class='neighborhood-str-list']//text()").extract()
            listing_address_full = product.xpath(".//div[@class='secondary-attributes']//address//text()").extract()
            address = join_address_elements(address_street + listing_address_full)
            contact_telephone = product.xpath(".//span[@class='biz-phone']//text()").extract_first()

            item = {}
            item['rank'] = rank
            item['name'] = name
            item['url'] = url
            item['rating'] = rating
            item['no_of_reviews'] = no_of_reviews
            item['tags'] = tags
            item['address'] = address
            item['contact_telephone'] = remove_white_spaces(contact_telephone)
            item['website_url'] = '-'
            search_url_page['page_results'].append(item)
            # inserting entire search result in single document thing won't work we visit detail page
            # for now disabling visiting detail page function , website-url to set to None
            # if visit_details_page:
            #     yield scrapy.Request(
            #         url=url,
            #         callback=self.get_data,
            #         meta={'item': item}
            #     )
            # # else:
            #     item['website_url'] = '-'
            #     yield item
        search_url_document['Results'].append(search_url_page)

        if int(no_of_pages_to_visit) == 1:
            yield search_url_document
        elif int(no_of_pages_to_visit > 1 or int(no_of_pages_to_visit) < 0):
            next_page = response.xpath(".//a[contains(@class,'pagination-links_anchor') "
                                       "and contains(@class,'next')]/@href").extract_first()
            if next_page:
                # print next_page
                yield scrapy.Request(
                    url=response.urljoin(next_page),
                    callback=self.parse,
                    meta={
                        'visit_details_page': visit_details_page,
                        'no_of_pages_to_visit': no_of_pages_to_visit - 1,
                        'search_url_id': search_url_id,
                        'search_url': search_url,
                        'search_group': search_group,
                        'serp_page': '%s' % (serp_page + 1),
                        'search_url_document': search_url_document,
                        'handle_httpstatus_list': [503]
                    }
                )
            else:
                yield search_url_document

