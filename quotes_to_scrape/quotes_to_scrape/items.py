# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    tags = scrapy.Field()
    author = scrapy.Field()
    quote = scrapy.Field()


class AuthorItem(scrapy.Item):
    fullname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()
