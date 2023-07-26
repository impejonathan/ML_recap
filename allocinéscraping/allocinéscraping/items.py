# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AllocinscrapingItem(scrapy.Item):
    titre = scrapy.Field()
    date = scrapy.Field()
    note_presse = scrapy.Field()
    note_spectateur = scrapy.Field()
    boxoffice = scrapy.Field()
    synopsis = scrapy.Field()

class AllocinescrapingItem(scrapy.Item):
    titre = scrapy.Field()
    entrees = scrapy.Field()
