# -*- coding: utf-8 -*-
import json

import scrapy
import time

import ele.items
import pymongo

#关于shop的爬虫主类

class ShopSpider(scrapy.Spider):
    name = 'shop'
    allowed_domains = ['ele.me']

    # 简餐便当 1
    # 本地菜系 8
    # 奶茶 -102
    # 面点 2
    # 包子 215
    # 包子 -14
    # 小吃鸭脖 235， -22

    # 日韩料理 229
    # 西餐 230
    # 披萨意面 211   -40
    # 米粉面馆 213   -24  -33
    # 甜品 9  -17
    # 面包蛋糕 12   -20
    # 奶茶果汁 11   -37  -16

    # 麻辣烫  214
    # 盖浇饭 209
    # 小龙虾 236
    # 川湘菜 221

    shop_base_url = "https://h5.ele.me/restapi/shopping/v3/restaurants?" \
                    "latitude={}&" \
                    "longitude={}&" \
                    "keyword=&" \
                    "offset={}&" \
                    "limit=8&" \
                    "extras[]=activities&" \
                    "terminal=h5&" \
                    "brand_ids[]=&" \
                    "restaurant_category_ids[]=-100"

    shop_index = 0

    # --------------汉口-----------------------------
    # 114.27258,30.61104 范湖地区
    # 范湖地区坐标点
    # current_latitude = 30.61104
    # current_longitude = 114.27258

    # 武汉武广商圈
    # current_latitude = 30.580458
    # current_longitude = 114.269997

    # # 武汉江汉路商圈
    # current_latitude = 30.584508
    # current_longitude = 114.286908

    # 武汉后湖永旺商圈
    # current_latitude = 30.630811
    # current_longitude = 114.283794

    # 三阳路
    current_latitude = 30.599738
    current_longitude = 114.300529

    # --------------武昌-----------------------------
    # 114.416441,30.484943 光谷软件园地区
    # 光谷软件园坐标点
    # current_latitude = 30.484943
    # current_longitude = 114.416441

    # 武汉徐东坐标点
    # current_latitude = 30.587975
    # current_longitude = 114.346233

    # 武汉中南坐标点
    # current_latitude = 30.53677
    # current_longitude = 114.331711

    # 武汉街道口商圈
    # current_latitude = 30.528023
    # current_longitude = 114.350494

    # 武汉司门口商圈
    # current_latitude = 30.547414
    # current_longitude = 114.298058

    # --------------汉阳-----------------------------
    # 武汉王家湾商圈
    # current_latitude = 30.562164
    # current_longitude = 114.207664

    # 武汉钟家村商圈
    # current_latitude = 30.55008
    # current_longitude = 114.265171

    # 武汉经开万达商圈
    # current_latitude = 30.506717
    # current_longitude = 114.173858

    # --------------大北京-----------------------------
    # 39.938612,116.328803 海淀西直门外大街
    # 海淀西直门外大街坐标点
    # current_latitude = 39.938612
    # current_longitude = 116.328803

    # 西单大悦城坐标点
    # current_latitude = 39.910891
    # current_longitude = 116.37298

    # #朝阳大悦城
    # current_latitude = 39.924548
    # current_longitude = 116.519035
    #
    # #东城区王府井大街
    # current_latitude = 39.916179
    # current_longitude = 116.411121
    #
    # # 望京soho
    # current_latitude = 39.996794
    # current_longitude = 116.48105
    #
    # # 五道口
    # current_latitude = 39.992065
    # current_longitude = 116.339075
    #
    # # 中关村
    # current_latitude = 39.983236
    # current_longitude = 116.30695

    # # 西二旗
    # current_latitude = 39.983236
    # current_longitude = 116.30695

    # # 公主坟
    # current_latitude = 39.912488
    # current_longitude = 116.303367

    # # 亚运村
    # current_latitude = 39.991761
    # current_longitude = 116.408027

    # # 三里屯
    # current_latitude = 39.932278
    # current_longitude = 116.453531

    # # 国贸
    # current_latitude = 39.912644
    # current_longitude = 116.458382

    # # 前门
    # current_latitude = 39.896653
    # current_longitude = 116.398323

    start_urls = [shop_base_url.format(current_latitude, current_longitude, shop_index)]

    def parse(self, response):
        response_text = response.body_as_unicode().strip()

        result = json.loads(response_text)

        items = result["items"]

        if len(items) != 0:
            for item in items:
                restaurant = item["restaurant"]

                shop = ele.items.ShopItem()
                shop["name"] = restaurant.get("name")
                shop["address"] = restaurant.get("address")
                shop["id"] = restaurant.get("id")
                shop["position"] = {"latitude": restaurant.get("latitude"), "longitude": restaurant.get("longitude")}
                shop["sales"] = restaurant.get("recent_order_num")

                yield shop

                time.sleep(0.2)

            self.shop_index = self.shop_index + 8
            next_url = self.shop_base_url.format(self.current_latitude, self.current_longitude, self.shop_index)

            time.sleep(1)

            yield scrapy.Request(url=next_url, callback=self.parse)

        # yield scrapy.Request(url="https://h5.ele.me/restapi/shopping/v2/menu?restaurant_id={}".format(shop["id"]),
        #                              callback=self.parse_foods)
        #
        #
        #
        # def parse_foods(self, response):
        #     response_text = response.body_as_unicode().strip()
        #
        #     result = json.loads(response_text)
        #
        #     for item in result:
        #         foods = item["foods"]
        #
        #         for f in foods:
        #             food = ele.items.FoodItem()
        #             food["product_id"] = f.get("virtual_food_id")
        #             food["shop_id"] = f.get("restaurant_id")
        #             food["name"] = f.get("name")
        #             food["month_sales"] = f.get("month_sales")
        #             food["rating_count"] = f.get("rating_count")
        #             food["sku"] = [{"sku_id": sku.get("sku_id"),
        #                             "name": sku.get("name"),
        #                             "food_id": sku.get("food_id"),
        #                             "price": sku.get("price")}
        #                            for sku in f.get("specfoods")]
        #
        #             yield food
