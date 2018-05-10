# -*- coding: utf-8 -*-
import csv
import json
import time
import scrapy

import ele


class ShopFoodSpider(scrapy.Spider):
    name = 'shop_food'
    allowed_domains = ['ele.me']
    # 添加start_requests方法，在内部直接执行yield Request(newUrl)就可以发起新的抓包请求
    # 如果重写start_requests方法，start_urls的请求就失效了
    # start_urls = ['http://ele.me/']
    food_base_url = "https://h5.ele.me/restapi/shopping/v2/menu?restaurant_id={}"

    miss_shop_id = ['837544', '837546', '160197359']
    miss_shop_name = ['靓靓蒸虾（沙湖店）', '靓靓蒸虾（光谷店）', '潜江五七油焖大虾欧亚达店']
    miss_id = 0

    out = open('miss_food.csv', 'a', newline='')
    writer = csv.writer(out, dialect='excel')
    title = ["菜品ID", "名称", "价格", "店铺ID", "店铺名称", "月售"]
    writer.writerow(title)
    # def parse(self, response):
    #     pass

    def start_requests(self):
        print(self.food_base_url.format(self.miss_shop_id[self.miss_id]))
        yield scrapy.Request(url=self.food_base_url.format(self.miss_shop_id[self.miss_id]))

    def parse(self, response):
        response_text = response.body_as_unicode().strip()

        result = json.loads(response_text)
        print('解析数据——---')
        for item in result:
            foods = item["foods"]

            for f in foods:
                shop_food = ele.items.FoodItem()
                shop_food["product_id"] = f.get("virtual_food_id")
                shop_food["shop_id"] = f.get("restaurant_id")
                shop_food["name"] = f.get("name")
                shop_food["month_sales"] = f.get("month_sales")
                shop_food["rating_count"] = f.get("rating_count")
                shop_food["sku"] = [{"sku_id": sku.get("sku_id"),
                                     "name": sku.get("name"),
                                     "food_id": sku.get("food_id"),
                                     "price": sku.get("price")}
                                    for sku in f.get("specfoods")]

                # print('得到店铺ID为 %s 的食物' %shop_food["shop_id"])
                # print(food)
                # with open("./miss_food.csv", "wb", newline='') as f:
                #     title = ["菜品ID", "名称", "价格", "店铺ID", "店铺名称", "月售"]
                #     writer = csv.writer(f)
                #     writer.writerow(title)

                product_id = shop_food["product_id"]
                food_name = shop_food["name"]
                price = shop_food["sku"][0]["price"]
                shop_id = shop_food["shop_id"]
                shop_name = self.miss_shop_name[self.miss_id]
                month_sales = shop_food["month_sales"]

                result_row = [product_id,
                              food_name,
                              price,
                              shop_id,
                              shop_name,
                              month_sales]

                try:
                    print(result_row)
                    self.writer.writerow(result_row)
                except Exception as ex:
                    print('write csv failed')
                    print(ex)
                # yield shop_food

                time.sleep(0.2)

            time.sleep(1)
        self.miss_id = 1 + self.miss_id
        print(self.food_base_url.format(self.miss_shop_id[self.miss_id]))
        yield scrapy.Request(url=self.food_base_url.format(self.miss_shop_id[self.miss_id]))
