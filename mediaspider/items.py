# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class VInfoItem(Item):
    VItem=Field()

class VInfoDynamicItem(Item):
    VItem=Field()

class ReplyInfoItem(Item):
    RItem=Field()

class DanmuInfoItem(Item):
    DItem=Field()

class UInfoItem(Item):
    UItem=Field()





