#!/usr/bin/env python
import datetime
import time
import requests

TASK_INTERVAL = 300
URL = 'http://127.0.0.1:8000/'
ENDPOINT = 'get_shop_statistics'


def crawl():
    response = requests.get(f'{URL}{ENDPOINT}')
    data = response.json()
    print(data)

    lines = []
    lines.append('Shop ID,Total Dollars,Total Sold Items,Order Count')
    for shop_id, values in data.items():
        line = f"{shop_id},{values['total_dollars']},{values['total_sold_items']},{values['order_count']}"
        lines.append(line)

    csv = '\n'.join(lines)
    now = datetime.datetime.now()
    filename = f'shop_statistics_{now.year}-{now.month:02}-{now.day:02}_{now.hour:02}{now.minute:02}.csv'
    with open(filename, 'w') as f:
        f.write(csv)


if __name__ == '__main__':
    while True:
        try:
            crawl()
        except:
            print('ERROR! CANNOT CRAWL DATA!')
        time.sleep(TASK_INTERVAL)
