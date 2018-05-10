# -*- coding: utf-8 -*-
import json

import pymongo
import scrapy
import time

import ele.items
#关于food的爬虫主类

class FoodSpider(scrapy.Spider):
    name = 'food'
    allowed_domains = ['ele.me']

    food_base_url = "https://h5.ele.me/restapi/shopping/v2/menu?restaurant_id={}"

    client = pymongo.MongoClient(host="localhost")
    db = client["food_syl_p100"]
    tb = db["shops"]
    shop_index = 0
    shops = iter(tb.find())
    # shops = iter([{"id": 1823562}, {"id": 1035891}])

    # 添加start_requests方法，在内部直接执行yield Request(newUrl)就可以发起新的抓包请求
    # 如果重写start_requests方法，start_urls的请求就失效了
    def start_requests(self):
        print(self.food_base_url.format(next(self.shops).get("id")))
        yield scrapy.Request(url=self.food_base_url.format(next(self.shops).get("id")))

    def parse(self, response):
        response_text = response.body_as_unicode().strip()

        result = json.loads(response_text)

        for item in result:
            foods = item["foods"]

            for f in foods:
                food = ele.items.FoodItem()
                food["product_id"] = f.get("virtual_food_id")
                food["shop_id"] = f.get("restaurant_id")
                food["name"] = f.get("name")
                food["month_sales"] = f.get("month_sales")
                food["rating_count"] = f.get("rating_count")
                food["sku"] = [{"sku_id": sku.get("sku_id"),
                                "name": sku.get("name"),
                                "food_id": sku.get("food_id"),
                                "price": sku.get("price")}
                               for sku in f.get("specfoods")]

                yield food

                time.sleep(0.2)

            time.sleep(1)

        yield scrapy.Request(url=self.food_base_url.format(next(self.shops).get("id")))
