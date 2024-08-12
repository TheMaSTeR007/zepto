# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZeptoItem(scrapy.Item):
    # define the fields for your item here like:
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    availability = scrapy.Field()
    product_price = scrapy.Field()
    discount = scrapy.Field()
    product_mrp = scrapy.Field()
