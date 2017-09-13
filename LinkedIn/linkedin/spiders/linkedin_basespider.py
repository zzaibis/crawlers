# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import scrapy


class LinkedInBaseSpider(scrapy.Spider):
    """
    base-spider for linked in login module
    """
    __metaclass__ = ABCMeta
    allowed_domains = ["linkedin.com"]
    start_urls = ("https://www.linkedin.com/uas/login",)
    custom_settings = {
        "DOWNLOAD_DELAY": 20
    }

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response=response,
            formname="login",
            formdata={
                'session_key': "user-email",
                'session_password': "password",
                'signin': "Sign In",
                'clickedSuggestion': "false",
            },
            callback=self.visit_urls
        )

    @abstractmethod
    def visit_urls(self, response):
        pass
