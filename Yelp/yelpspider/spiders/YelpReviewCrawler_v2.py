
import scrapy
import unicodedata 
import json
from pymongo import MongoClient
from yelpspider.helpers.network_manager import get_start_urls_biz, update_search_param_status_biz
from yelpspider.helpers.string_processor import join_address_elements, remove_white_spaces

def generate_start_urls(domain):
    start_url = []
    urls = json.loads(get_start_urls_biz(domain=domain))
    for url in urls:
        start_url.append({'url': url['search_url'],
                          'search_url_id': url['id'],
                          'search_group': url['search_group']})
    return start_url

class Yelpreview(scrapy.Spider):
   handle_httpstatus_list = [500, 502,503]
   name = "yelpbiz"
   domain = "yelpbiz"
   allowed_domains = ["www.yelp.com"]
   requests_queue = []
   def start_requests(self):
        urls = generate_start_urls(self.domain)
        for url in urls:
            print url
            self.requests_queue.append(scrapy.Request(
                url=url['url'],
                callback = self.parse,
                meta={
                    'search_url_id': url['search_url_id'],
                    'search_group': url['search_group'],
                    'search_url': url['url'],
                    'handle_httpstatus_list': [503]
                },
                dont_filter=True
            ))
        while self.requests_queue:
            yield self.requests_queue.pop()

   def parse(self, response):
        search_url_id = response.meta['search_url_id']
        try:        
            document = response.meta['document']
            count = response.meta['count']
            pages = response.meta['pages']
            Url = response.meta['Url']
        except:
            document = {}
            document['search_group'] = response.meta['search_group']
            document['link'] = response.xpath('//span[@class="biz-website"]/a/text()').extract_first()
            document['reviews'] = []
            document['yelp_url'] = response.url
            count = 1
            try:
                pages = response.xpath('//div[@class="page-of-pages arrange_unit arrange_unit--fill"]/text()').extract_first().strip()
            except:
                update_search_param_status_biz(search_param_id=search_url_id, domain=self.domain,status=2)
            pages = float(pages.rsplit(' ',1)[1])
            Url = response.url
            #specialities and owner info
            t = {}
            t1 = {}
            own = {}
            t1['history']=''
            l =[]
            c = 0
            sell =  response.xpath('//div[@class="from-biz-owner-content"]/p')
            for s in sell:
                if (c==0):
                 t1['specialities'] = (''.join(s.xpath('./text()').extract())).strip()
            
                if (c==1 or c==2):
                    try:
                        l.append(s.xpath('./text()').extract())
                    except:
                        pass
                if(c==3):
                    own['description'] = (''.join(s.xpath('./text()').extract())).strip()
                c=c+1
            
            for el in sum(l, []):
                t1['history'] += (el.strip())
            try:
                own['name'] = response.xpath('//div[@class="meet-business-owner"]//span/text()').extract_first().strip().encode('utf8')
                own ['role'] = response.xpath('//div[@class="business-owner-role"]/text()').extract_first().strip().encode('utf8')
                own['description'].strip().encode('utf8')
            except:
                pass
            try:
                t1['specialities'].strip()
                document['specialities'] = t1['specialities'].encode('utf8')
            except:
                pass
            if len(own)>0:
                document['owner'] = own 
            if len(t1['history']) > 0:
                document['history'] = t1['history'].encode('utf8') 

            #adress and contact info
            try:
                document['gym_phn'] = response.xpath('//span[@class="biz-phone"]/text()').extract_first().strip().encode('utf8')
            except:
                document['gym_phn'] = ''
            document['gym_name'] = response.xpath('//div[@class="biz-page-header clearfix"]//h1/text()').extract_first().strip().encode('utf8') 
            gym_addr = (''.join(response.xpath('//li[@class="map-box-address u-space-l4"]//text()').extract()))
            document['gym_addr'] = " ".join(gym_addr.split()).encode('utf8') 


            #business info
            sel = response.xpath('//div[@class="ywidget"]/ul//dl')
            for se in sel:
                t[se.xpath('dt/text()').extract_first().strip()] = se.xpath('dd/text()').extract_first().strip().encode('utf8') 
            document['business_info'] =  t
            
        
        for sel in response.xpath('//div[@class="review-wrapper"]'):
            tmp = {}
            rev = sel.xpath('div[@class="review-content"]/p/text()').extract()
            tmp['review'] = ''.join(rev)
            tmp['date'] = sel.xpath('.//span[@class="rating-qualifier"]/meta/@content').extract_first()
            rating = sel.xpath('.//div[@class="rating-very-large"]/meta/@content').extract_first()
            try:
                tmp['rating'] = float(rating)
            except:
                tmp['rating'] = 0.0

            counts = sel.xpath(".//span[contains(.//text(), 'Useful')]/../span[@class='count']/text()").extract_first()
            try:
                tmp['useful'] = float(counts)
            except:
                tmp['useful'] = 0.0
            
            document['reviews'].append(tmp)
        
        print pages
        if pages == 1.0:
            update_search_param_status_biz(search_param_id=search_url_id, domain=self.domain,status=2)
            yield document
            MongoClient('mongodb://104.198.195.35:27017').Falcon.Flight3.insert(document)
        if response.xpath('//span[@class="pagination-label responsive-hidden-small pagination-links_anchor"]/text()').extract_first() == 'Next':
            print 'Next'
            url = Url + "?start=" + str(count*20)
            #print "url = ",url
            yield scrapy.Request(url, callback=self.parse, meta = {'pages' : pages - 1.0, 'document' : document, 'count' : count + 1, 'Url' : Url , 'handle_httpstatus_list': [503], 'search_url_id' : search_url_id})
        


