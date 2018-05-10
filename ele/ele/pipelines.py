# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#处理内容
import csv

import pymongo
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from ele.items import ShopItem, FoodItem


class JsonSaverPipeline(object):

    def __init__(self):
        self.file = open("result_ele.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, ShopItem):
            self.exporter.export_item(item)

        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class DbSaverPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(host="localhost")
        self.db = client["food_syl_p100"]
        self.shops = self.db["shops"]
        self.foods = self.db["foods"]

    def process_item(self, item, spider):

        if isinstance(item, ShopItem):
            data = dict(item)
            try:
                result = self.shops.replace_one({"id": data.get("id")}, data, upsert=True)
            except Exception as ex:
                print(ex)
        elif isinstance(item, FoodItem):
            data = dict(item)

            try:
                result = self.foods.replace_one({"shop_id": data.get("shop_id"), "product_id": data.get("product_id")},
                                                data, upsert=True)

            except Exception as ex:
                print(ex)

        return item

    def close_spider(self, spider):
        pass


class CsvSaverPipeline(object):

    def __init__(self):
        self.file = open("miss_shop_food2.csv", "wb")
        self.exporter = CsvItemExporter(self.file, encoding="utf-8")
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        # print(item)
        if isinstance(item, FoodItem):
            self.exporter.export_item(item)

            with open("./miss_shop_food1.csv", "w", newline='') as f:
                title = ["菜品ID", "名称", "价格", "店铺ID", "店铺名称", "月售"]

                writer = csv.writer(f)

                writer.writerow(title)

                shop_id = item.get("shop_id")

                # shop = self.shop_tb.find({"id": shop_id})

                # shop_name = ""
                shop_name = item[0].get("name")

                price = item.get("sku")[0]["price"]

                result_row = [item.get("product_id"),
                              item.get("name"),
                              price,
                              shop_id,
                              shop_name,
                              item.get("month_sales")]

                print(result_row)
                try:
                    writer.writerow(result_row)
                except Exception as ex:
                    print(ex)

    def close_spider(self, spider):
        pass
