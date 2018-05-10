# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
#暂存爬取的数据
import scrapy


class ShopItem(scrapy.Item):

    # 店铺名称
    name = scrapy.Field()

    # 店铺地址
    address = scrapy.Field()

    # 店铺ID
    id = scrapy.Field()

    # GPS坐标
    position = scrapy.Field()

    # 店铺月售
    sales = scrapy.Field()


class FoodItem(scrapy.Item):

    # 菜品ID
    product_id = scrapy.Field()

    # 店铺ID
    shop_id = scrapy.Field()

    # 菜品名称
    name = scrapy.Field()

    # 菜品价格
    price = scrapy.Field()

    # 菜品月售
    month_sales = scrapy.Field()

    # 推荐数
    rating_count = scrapy.Field()

    # SKU
    sku = scrapy.Field()
