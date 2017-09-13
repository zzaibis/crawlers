# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy
from .linkedin_basespider import LinkedInBaseSpider
from linkedin.helpers.network_manager import get_start_urls, update_search_param_status
import json


def generate_start_urls(domain):
    start_url = []
    urls = json.loads(get_start_urls(domain=domain))
    for url in urls:
        start_url.append({'url': url['search_url'],
                          'search_url_id': url['id'],
                          'search_group': url['search_group']})
    # start_url.append({'url': "https://www.linkedin.com/in/dharmeshpandav",
    #                   'search_url_id': 1,
    #                   'search_group': "default"})
    return start_url


class LinkedInIndividualProfileSpider(LinkedInBaseSpider):
    domain = 'linked_in_individual'
    name = "linkedin_person_profile"
    requests_queue = []

    def visit_urls(self, response):
        # for url in ["https://www.linkedin.com/in/sandipdasfreelancer", "https://www.linkedin.com/in/mrbhoot"]:
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

        person_id = re.search(r'([^/]*$)', response.url)
        person_id = person_id.group(1) if person_id else ""
        name = ''.join(response.xpath(".//div[@id='name']//text()").extract())
        title = ''.join(response.xpath(".//div[@id='headline']//text()").extract())
        location = ''.join(response.xpath(".//dt[text()='Location']/following-sibling::dd[1]//text()").extract())
        industry = ''.join(response.xpath(".//dt[text()='Industry']/following-sibling::dd[1]//text()").extract())
        current_organization = ''.join(
            response.xpath(".//tr[@id='overview-summary-current']//li//text()").extract())
        current_organization_link = ''.join(
            response.xpath(".//tr[@id='overview-summary-current']//a/@href").extract())

        current_organization_link = response.urljoin(current_organization_link)
        previous_organizations = response.xpath(".//tr[@id='overview-summary-past']//li")
        previous_organizations = [{'org_name': ''.join(org.xpath(".//text()").extract()),
                                   'org_url': response.urljoin(org.xpath(".//a/@href").extract_first()),
                                   'person_id': person_id}
                                  for org in previous_organizations]

        summary = response.xpath(".//div[@id='summary-item']")
        summary_text = ''.join(summary.xpath(".//text()").extract())
        summary_html = ''.join(summary.extract())

        languages = response.xpath(".//div[@id='languages']//li[@class='section-item']")
        languages = [{'name': lang.xpath(".//h4//text()").extract_first(),
                      'proficiency': lang.xpath(".//*[@class='languages-proficiency']/text()").extract_first(),
                      'person_id': person_id}
                     for lang in languages]
        skills = response.xpath(".//div[@id='background-skills']//li[@data-endorsed-item-name]")
        skills = [{'name': skill.xpath(".//a[@class='endorse-item-name-text']//text()").extract_first(),
                   'skill_url': response.urljoin(
                       skill.xpath(".//a[@class='endorse-item-name-text']/@href").extract_first()),
                   'person_id': person_id}
                  for skill in skills]

        experiences = response.xpath(".//div[@id='background-experience']/div")
        experiences = [{
            'title': ''.join(experience.xpath(".//header//h4//text()").extract()),
            'title_url': response.urljoin(experience.xpath(".//header//h4//a/@href").extract_first()),
            'company': ''.join(experience.xpath(".//header//h5//text()").extract()),
            'company_url': response.urljoin(experience.xpath(".//header//h5//a/@href").extract_first()),
            'duration': ''.join(experience.xpath(".//*[@class='experience-date-locale']//text()").extract()),
            'description_text': ''.join(experience.xpath(".//*[contains(@class,'description')]//text()").extract()),
            'description_html': ''.join(experience.xpath(".//*[contains(@class,'description')]").extract()),
            'person_id': person_id
            }
                       for experience in experiences]

        educations = response.xpath(".//div[@id='background-education']/div")
        educations = [{
            'school': ''.join(education.xpath(".//header//h4//text()").extract()),
            'school_url': response.urljoin(education.xpath(".//header//h4//a/@href").extract_first()),
            'course_name': ''.join(education.xpath(".//header//h5//text()").extract()),
            'duration': ''.join(education.xpath(".//*[@class='education-date']//text()").extract()),
            'description_text': ''.join(
                education.xpath(".//p[contains(@class,'notes') or contains(@class,'activities')]//text()").extract()),
            'description_html': ''.join(
                education.xpath(".//p[contains(@class,'notes') or contains(@class,'activities')]").extract()),
            'person_id': person_id
            }
                      for education in educations]

        recommendations = response.xpath(".//div[@id='endorsements']//div[@class='endorsement-full']")
        recommendations = [{'recommendation_text': ''.join(recommendation.xpath(".//blockquote//text()").extract()),
                            'recommendation_html': ''.join(recommendation.xpath(".//blockquote//text()").extract()),
                            'who_endorsed': ''.join(recommendation.xpath(".//hgroup//h5//text()").extract()),
                            'who_endorsed_url': response.urljoin(
                                recommendation.xpath(".//hgroup//h5//a/@href").extract_first()),
                            'who_endorsed_title': ''.join(recommendation.xpath(".//hgroup//h6//text()").extract()),
                            'when': ''.join(
                                recommendation.xpath(".//span[@class='endorsement-date']//text()").extract()),
                            'person_id': person_id
                           } for recommendation in recommendations]


        main_item = {}
        main_item['search_url'] = search_url
        main_item['search_url_id'] = search_url_id
        main_item['search_group'] = search_group
        main_item['person_id'] = person_id
        main_item['url'] = response.url
        main_item['name'] = name
        main_item['title'] = title
        main_item['location'] = location
        main_item['industry'] = industry
        main_item['current_organization'] = current_organization
        main_item['current_organization_link'] = current_organization_link
        main_item['summary_text'] = summary_text
        main_item['summary_html'] = summary_html
        main_item['created_at'] = datetime.utcnow()

        item = {}
        item['main'] = main_item
        item['previous_organizations'] = previous_organizations
        item['recommendations'] = recommendations
        item['languages'] = languages
        item['skills'] = skills
        item['experiences'] = experiences
        item['educations'] = educations
        item['recommendations'] = recommendations

        yield item
