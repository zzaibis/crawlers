# -*- coding: utf-8 -*-
import json
import scrapy
from .linkedin_basespider import LinkedInBaseSpider
from linkedin.helpers.network_manager import get_start_urls, update_search_param_status


def generate_start_urls(domain):
    start_url = []
    urls = json.loads(get_start_urls(domain=domain))
    for url in urls:
        start_url.append({'url': url['search_url'],
                          'search_url_id': url['id'],
                          'search_group': url['search_group']})
    # start_url.append({'url': "https://www.linkedin.com/company/4501",
    #                   'search_url_id': 1,
    #                   'search_group': "default"})
    return start_url


class LinkedinCompanyProfileSpider(LinkedInBaseSpider):
    domain = 'linked_in_company'
    name = "linkedin_company_profile"
    requests_queue = []

    def visit_urls(self, response):
        urls = generate_start_urls(self.domain)
        for url in urls:
            yield scrapy.Request(
                url=url['url'],
                callback=self.parse2,
                meta={
                    'search_url_id': url['search_url_id'],
                    'search_group': url['search_group'],
                    'search_url': url['url'],
                    'handle_httpstatus_list': [999]
                }
            )

        while self.requests_queue:
            yield self.requests_queue.pop()

    def parse2(self, response):
        search_url = response.meta['search_url']
        search_url_id = response.meta['search_url_id']
        search_group = response.meta['search_group']
        if response.status == 200:
            update_search_param_status(search_param_id=search_url_id, domain=self.domain)
        # data = response.xpath(".//code[@id='stream-feed-embed-id-content']//comment()").extract_first()
        # data2 = response.xpath(".//code[@id='stream-about-section-embed-id-content']//comment()").extract_first()

        # data = data.replace("<!--", "").replace("-->","")
        # data2 = data2.replace("<!--", "").replace("-->","")

        # data = json.loads(data)
        # data2 = json.loads(data2)
        # load data from # in linkedin
        company_url = response.url
        data = response.xpath(".//code[@id='stream-promo-top-bar-embed-id-content']//comment()").extract_first()
        data = data.replace("<!--", "").replace("-->", "")
        data = json.loads(data)
        url = data.get('homeUrl')
        company = data.get('companyName')
        company_id = data.get('companyId')
        company_type = data.get('companyType')
        c_type = data.get('type')
        industry = data.get('industry')
        description = data.get('description')
        website = data.get('website')
        year_founded = data.get('yearFounded')
        address_block = data.get('headquarters')
        if address_block:
            address = ", ".join(v for k, v in address_block.iteritems())
            city = address_block.get('city')
            country = address_block.get('country')
            state = address_block.get('state')
            zip_code = address_block.get('zip')
        else:
            address, city, country, state, zip_code = [None] * 5
        image = "https://media.licdn.com/media/%s" % data.get('heroImage')
        company_logo = "https://media.licdn.com/mpr/mpr/shrink_200_200/%s" % data.get('squareLogo')
        followers = data.get('followerCount')
        employees = data.get('size')

        item = {}
        item['search_url'] = search_url
        item['search_url_id'] = search_url_id
        item['search_group'] = search_group
        item['url'] = url
        item['company_url'] = company_url
        item['company'] = company
        item['company_logo'] = company_logo
        item['company_id'] = company_id
        item['company_type'] = company_type
        item['employees'] = employees
        item['website'] = website
        item['industry'] = industry
        item['c_type'] = c_type
        item['city'] = city
        item['state'] = state
        item['zip_code'] = zip_code
        item['country'] = country
        item['image'] = image
        item['followers'] = followers
        item['description'] = description
        item['year_founded'] = year_founded
        item['address'] = address
        yield item
