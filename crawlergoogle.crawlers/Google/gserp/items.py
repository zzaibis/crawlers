# __author__ = 'Dharmesh Pandav'
from scrapy.item import Item, Field


class SerpPages(Item):
    rank = Field()
    url = Field()
    title = Field()
    short_description = Field()
    search_file_type = Field()
    search_word = Field()
    search_word_id = Field()
    search_page_no = Field()
    missing_word = Field()
    search_url = Field()
    created_at = Field()


class Link(Item):
    url = Field()


class SerpImagePages(Item):
    rank = Field()
    url = Field()
    title = Field()
    image_url = Field()
    short_description = Field()
    search_file_type = Field()
    search_image_id = Field()
    search_image_name = Field()
    search_page_no = Field()
    search_url = Field()
    created_at = Field()


class SerpImageSearch(Item):
    image_url = Field()
    image_provider = Field()
    search_word_id = Field()
    search_word = Field()

