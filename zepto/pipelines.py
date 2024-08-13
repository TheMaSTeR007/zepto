# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from zepto.items import ZeptoItem
from zepto.customUtils import insert_into


class ZeptoPipeline:
    def process_item(self, item, spider):
        # Determine the table based on item type
        if isinstance(item, ZeptoItem):
            data_table_name = 'products_data_test_final'
        else:
            print('Skipped Processing...')
            # If the item type is unknown, skip processing
            return item

        copy_item = item.copy()

        cols = ', '.join(copy_item.keys())
        values = tuple(copy_item.values())
        placeholders = ', '.join(['%s'] * len(copy_item))

        insert_query = insert_into(table_name=data_table_name, cols=cols, placeholders=placeholders)

        try:
            print(f'Inserting {data_table_name} Data into DB Table...')
            spider.cursor.execute(query=insert_query, args=values)
            print('Inserted Data Successfully.')
        except Exception as e:
            print(f'Error inserting {data_table_name} data: {e}')
            # Optionally log the error or take other actions

        return item
