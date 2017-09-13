# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from gserp.helpers.string_processor import remove_white_spaces
from w3lib.url import url_query_parameter
from gserp.helpers.network_manager import get_start_urls, update_search_param_status
import json


def generate_start_urls(base_url, domain):
    start_url = []
    urls = json.loads(get_start_urls(domain=domain))
    for serp_param in urls:
        search_image_name = serp_param.search_image_name
        search_image_id = serp_param.id
        search_image_url = serp_param.search_image_url
        image_server_ip = serp_param.image_server_ip if serp_param.image_server_ip else "http://localhost"
        image_base_path = serp_param.image_base_path
        if image_base_path:
            base_path = "%s/%s" % (image_server_ip, image_base_path)
            url = base_url % (base_path, search_image_url)
        else:
            url = base_url % (image_server_ip, search_image_url)
        start_url.append({'url': url,
                         'search_image_id': search_image_id,
                          'search_image_name': search_image_name,
                          'search_group': serp_param.search_group,
                          'no_of_pages_per_keyword': serp_param.no_of_pages_per_keyword
                          })
    return start_url


class GscraperImagesSpiderV3(scrapy.Spider):
    name = "gscraper_images_v3"
    allowed_domains = ["google.com"]
    domain = "gimages"
    # start_urls = (
    #     'https://images.google.com/searchbyimage?image_url=http://104.197.118.137/image/bulb-1239423_960_720.jpg&encoded_image=&image_content=&filename=&hl=en',
    # )
    # base_ip = "http://104.197.118.137"
    no_of_pages_per_keyword = 4
    requests_queue = []
    base_url = 'https://images.google.com/searchbyimage?' \
        'image_url=%s/%s' \
        '&encoded_image=' \
        '&image_content=' \
        '&filename=' \
        '&hl=en'

    def start_requests(self):
        urls = generate_start_urls(self.base_url, self.domain)
        for url in urls:
            self.requests_queue.append(scrapy.Request(
                url=url['url'],
                callback=self.parse,
                dont_filter=True,
                meta={'search_image_id': url['search_image_id'],
                      'search_image_name': url['search_image_name'],
                      'search_group': url['search_group'],
                      'no_of_pages_per_keyword': url['no_of_pages_per_keyword']
                      }
            ))
        while self.requests_queue:
            yield self.requests_queue.pop()

    def parse(self, response):
        # FIXED FIX-ME TODO need to add search group to database for image
        search_image_name = response.meta['search_image_name']
        search_image_id = response.meta['search_image_id']
        search_group = response.meta['search_group']
        no_of_pages_per_keyword = response.meta['no_of_pages_per_keyword']
        start_page = url_query_parameter(response.url, 'start')
        serp_page = int(start_page)/10 + 1 if start_page else 1
        sites = response.xpath('//div[@class="srg"]/div[@class="g"]')

        if response.status == 200:
            update_search_param_status(search_param_id=search_image_id, domain=self.domain, status=2)

        if not response.meta.get("search_image_document"):
            search_image_document = {}
            search_image_document['search_image_name'] = search_image_name
            search_image_document['search_image_id'] = search_image_id
            search_image_document['search_group'] = search_group
            search_image_document['Results'] = []
        else:
            search_image_document = response.meta["search_image_document"]

        search_image_page = {}
        search_image_page['search_page_no'] = serp_page
        search_image_page['page_results'] = []
        for site in sites:
            rank = sites.index(site) + 1
            url = site.xpath(".//h3[@class='r']/a/@href").extract_first()
            title = remove_white_spaces(site.xpath(".//h3[@class='r']/a/text()").extract_first())
            image_url = response.urljoin(site.xpath(".//div[@class='th _lyb']/a/@href").extract_first())
            image_url = url_query_parameter(image_url, 'imgurl')
            short_description = ''.join(site.xpath(".//span[@class='st']//text()").extract())
            created_at = datetime.utcnow()

            item = {}
            item['rank'] = rank
            item['url'] = url
            item['title'] = title
            item['image_url'] = image_url
            item['short_description'] = short_description
            item['created_at'] = created_at
            search_image_page['page_results'].append(item)

        search_image_document['Results'].append(search_image_page)

        next_page = response.xpath(".//a[@id='pnnext']/@href").extract_first()
        start_index = url_query_parameter(response.url,'start')
        start_index = int(start_index) if start_index else None
        if next_page and start_index < (no_of_pages_per_keyword - 1) * 10:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse,
                dont_filter=True,
                meta={'search_image_id': search_image_id,
                      'search_image_name': search_image_name,
                      'search_group': search_group,
                      'no_of_pages_per_keyword': no_of_pages_per_keyword,
                      'search_image_document': search_image_document}
            )
        else:
            yield search_image_document
