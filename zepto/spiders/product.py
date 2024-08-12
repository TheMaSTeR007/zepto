from typing import Iterable

import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from zepto.customCookies import cookies_list

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
    def __init__(self):
        super().__init__()

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
        rows = [
            'https://www.zeptonow.com/pn/nandini-fresh-toned-fresh-milk-pouch-blue/pvid/25eb526c-9c26-48cd-95a3-8e4058910f8a',
            'https://www.zeptonow.com/pn/deep-rooted-residue-free-amaranthus-green/pvid/afc7b9b8-99b4-4f64-8653-cd0d45edaf7e',
            'https://www.zeptonow.com/pn/adidas-india-cricket-t20-fan-mens-100-recycled-polyester-jersey-l-heatrdy/pvid/460cba41-a438-4592-a2a0-81438b76c503',
            'https://www.zeptonow.com/pn/classic-connect-cigarette/pvid/80f5c93c-8302-41b5-85f5-4c1ba12e4306',
            'https://www.zeptonow.com/pn/doms-x1-pencil-10-pc-x-2-combo/pvid/ac4946a8-0b66-411d-801c-ac3c4c2c1894',
            'https://www.zeptonow.com/pn/youbella-women-stylish-latest-design-trendy-multi-layer-necklace-jewellery-gold-plated-multi-strand/pvid/4b4cd0ef-8d9e-4f7f-a8e1-7db59e5c569d',
            'https://www.zeptonow.com/pn/teal-by-chumbak-ombre-aztec-watch-white/pvid/f4b38290-9733-45b9-8c87-b0bf7501783b',
            'https://www.zeptonow.com/pn/disney-frozen-2-printed-headband-blue/pvid/0f562afc-79ba-467a-8964-57fd46dc2496',
            'https://www.zeptonow.com/pn/mens-chain-black/pvid/a2739303-8c84-471a-97b5-10aeb7bf4c81',
            'https://www.zeptonow.com/pn/blue-stone-mens-chain-bracelet-silver/pvid/51399c84-9be3-44fc-a8a7-57b76f7ba2f1',
            'https://www.zeptonow.com/pn/youbella-jewellery-organiser-pu-leather-zipper-portable-storage-box-case-style-2-pink/pvid/9e4ca9ee-152a-43aa-bfaf-5b3bf3fef3fa',
            'https://www.zeptonow.com/pn/just-herbs-party-ready-nail-paint-set/pvid/3b26af0b-03ee-4c51-86ad-88833ccbd6b2',
            'https://www.zeptonow.com/pn/sugar-super-shimmer-kit-pack-of-5/pvid/8b4cc8e1-efc3-4766-a256-63835dce6622',
            'https://www.zeptonow.com/pn/renee-bold-4-4-in-1-kajal/pvid/70922f37-76b3-4075-a3a3-fdadf06c4c31',
            'https://www.zeptonow.com/pn/sheba-rich-skipjack-salmon-in-sasami-wet-cat-food/pvid/727be53e-6979-46a0-9a78-48038dc88f35',
            'https://www.zeptonow.com/pn/nootie-training-pads45x6010pcs/pvid/f809ba67-b3c0-41b9-b14a-3a53f1ff8985',
            'https://www.zeptonow.com/pn/kama-sutra-ultra-thin-condoms/pvid/cc9c9967-ff87-464a-bb59-2dc0d002cef9',
            'https://www.zeptonow.com/pn/carlton-london-women-blush-deodorant/pvid/83b78563-a616-4ca8-8177-8fd7f99d74e9',
            'https://www.zeptonow.com/pn/svish-hair-removal-spray-for-men-made-safe-certified/pvid/b61ead42-ba2e-4acd-906e-f41908765d8b',
            'https://www.zeptonow.com/pn/tide-jasmine-rose-detergent-powder/pvid/72320d9c-f67f-4f87-9643-1f3f147d7f7f',
            'https://www.zeptonow.com/pn/la-carne-chicken-piri-piri/pvid/d02b5699-763b-4bf0-b3f3-1e943cec202f',
            'https://www.zeptonow.com/pn/relish-chicken-breast-boneless500gms-relish-chicken-drumstick1pc-combo/pvid/91aa288d-1deb-41c5-a359-2a40590c0ac2'
        ]
        print(len(rows))
        cookies = cookies_list
        cookie_count = 1
        for product_url in rows:
            # product_url = row[999]  # Assuming the URL is in the third column
            print('Working on:', product_url)
            for cookie in cookies:
                # Yield a new request for each URL, which Scrapy will process asynchronously
                yield scrapy.Request(
                    url=product_url,
                    method='GET',
                    cookies=cookie,
                    callback=self.parse,  # The parse method will handle the response
                    dont_filter=True,
                    meta={
                        'count': cookie_count
                    }
                )
                cookie_count += 1

    def parse(self, response):
        count = response.meta['count']
        print('Cookie no:', count)
        print('response url:', response.url)
        product_url = get_product_url(response)
        product_name = get_product_name(response)
        availability = get_availability(response)
        product_price = get_product_price(response)
        discount = get_discount(response)
        product_mrp = get_product_mrp(response)

        print(product_url)
        print(product_name)
        print(availability)
        print(product_price)
        print(discount)
        print(product_mrp)
        print('-' * 100)


if __name__ == '__main__':
    execute(f'scrapy crawl {ProductSpider.name}'.split())
