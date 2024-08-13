import json
import os.path
import time
from typing import Iterable
import pandas as pd

import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from zepto.items import ZeptoItem


def get_product_url(response):
    product_url = response.xpath('//link[@rel="canonical"]/@href').get()
    return product_url if product_url else 'N/A'


def get_product_name(response):
    product_name = response.xpath('//div[@data-testid="pdp-product-name"]/h1/text()').get()
    return product_name if product_name else 'N/A'


def get_availability(response):
    availability = response.xpath('//button[@aria-label="Add"]/div/span/text() | //div[contains(@class, "tag_tag__Y2gMh") and contains(text(), "Out of Stock")]/text() | //button[@aria-label="Notify"]//span/text()').get()
    if availability.strip().lower() in ['out of stock', 'notify']:  # If Item is NOT available
        return "OutOfStock"
    elif availability.strip().lower() == 'add':  # If Item is available
        return "inStock"
    else:
        return "N/A"


def get_product_price(response):
    product_price = response.xpath('//h4[@data-test-id="pdp-selling-price"]/text()').get()
    return product_price if product_price else 'N/A'


def get_discount(response):
    discount = response.xpath('//div[@class="flex items-center"]/div/text()').get()
    return discount if discount else 'N/A'


def get_product_mrp(response):
    product_mrp = response.xpath('//p[@data-testid="pdp-discounted-price"]/text()').get()
    return product_mrp if product_mrp else 'N/A'


class ProductSpider(scrapy.Spider):
    name = "product"

    # allowed_domains = ["xyz.com"]
    # start_urls = ["https://xyz.com"]
    def __init__(self, start_id=None, end_id=None):
        super().__init__()
        self.start_id = int(start_id)
        self.end_id = int(end_id)

        # Connect to the MySQL database
        self.client = pymysql.Connect(
            database='zepto_db',
            user='root',
            password='actowiz',
            autocommit=True  # Enable autocommit mode
        )
        self.cursor = self.client.cursor()  # Create a cursor object to interact with the database

    def start_requests(self) -> Iterable[Request]:
        # fetch_table = 'products_raw_data'
        # # Query to select URLs that are pending for scraping
        # fetch_query = f'''SELECT * FROM {fetch_table};'''
        # self.cursor.execute(query=fetch_query)
        # rows = self.cursor.fetchall()
        # print(f'Fetched {len(rows)} data.')

        product_urls = pd.read_excel(io=r'C:\Users\jaimin.gurjar\Downloads\zepto_grocery.xlsx', sheet_name=' zepto')['Zepto '].dropna()[self.start_id: self.end_id]
        # product_urls = pd.read_excel(io=r'C:\Users\jaimin.gurjar\Downloads\zepto_grocery.xlsx', sheet_name=' zepto')['Zepto '].dropna()[:10]
        print('Heloooo')
        cookies_json_path = os.path.join(r'C:\Users\jaimin.gurjar\Actowiz Training Projects (using Scrapy)\zepto\zepto', 'cookies_json.json')
        with open(cookies_json_path, 'r') as file:
            list_of_cookies = json.loads(file.read())
        print('Cookies read done... !!')
        cookies_list = list_of_cookies
        print('Byeeee')
        print(len(product_urls))
        for product_url in product_urls:
            print('Working on: ', product_url)
            cookie_count = 1
            for cookie_data in cookies_list:
                cookie_dict = cookie_data['cookie_dict']
                pincode = cookie_data['pincode']
                # Yield a new request for each URL, which Scrapy will process asynchronously
                yield scrapy.Request(
                    url=product_url,
                    method='GET',
                    callback=self.parse,  # The parse method will handle the response
                    dont_filter=True,
                    cookies=cookie_dict,
                    meta={
                        "impersonate": "chrome110",
                        "count": cookie_count,
                        "pincode": pincode
                    }
                )
                cookie_count += 1

    def parse(self, response):
        cookie_num = response.meta['count']
        pincode = response.meta['pincode']
        print('using cookie:', cookie_num)
        print('response url:', response.url)
        product_url = get_product_url(response)
        product_name = get_product_name(response)
        availability = get_availability(response)
        product_price = get_product_price(response)
        discount = get_discount(response)
        product_mrp = get_product_mrp(response)

        Zepto_Data_Item = ZeptoItem()
        Zepto_Data_Item['product_url'] = product_url
        Zepto_Data_Item['product_name'] = product_name
        Zepto_Data_Item['availability'] = availability
        Zepto_Data_Item['product_price'] = product_price
        Zepto_Data_Item['discount'] = discount
        Zepto_Data_Item['product_mrp'] = product_mrp
        Zepto_Data_Item['pincode'] = pincode

        print(product_url)
        print(product_name)
        print(availability)
        print(product_price)
        print(discount)
        print(product_mrp)
        print(pincode)
        yield Zepto_Data_Item
        print('-' * 100)


if __name__ == '__main__':
    execute(f'scrapy crawl {ProductSpider.name}'.split())
