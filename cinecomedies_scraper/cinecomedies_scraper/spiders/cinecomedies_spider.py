import scrapy


class CinecomediesSpiderSpider(scrapy.Spider):
    name = "cinecomedies_spider"
    allowed_domains = ["cinecomedies.com"]
    start_urls = ["http://cinecomedies.com/"]

    def parse(self, response):
        pass
