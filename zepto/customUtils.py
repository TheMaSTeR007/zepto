products_data_test_table_query = '''CREATE TABLE products_data_test (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    product_url VARCHAR(255),
                                    product_name VARCHAR(255),
                                    availability VARCHAR(255),
                                    product_price VARCHAR(255),
                                    discount VARCHAR(255),
                                    product_mrp VARCHAR(255)
                                    );'''


# Dynamic Insert query
def insert_into(table_name, cols, placeholders):
    insert_query = f'''INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders});'''
    return insert_query
