import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import subprocess

def run_spider():
    subprocess.run(["scrapy", "crawl", "senscritique", "-O", "senscritique.csv"])

class SenscritiqueSpider(CrawlSpider):
    name = "senscritique"
    allowed_domains = ["www.senscritique.com"]
    base_urls = [
    "https://www.senscritique.com/liste/box_office_france_2000/1532844",
    "https://www.senscritique.com/liste/box_office_france_2001/1532849",
    "https://www.senscritique.com/liste/box_office_france_2002/1532854",
    "https://www.senscritique.com/liste/box_office_france_2003/1532859",
    "https://www.senscritique.com/liste/box_office_france_2004/1532868",
    "https://www.senscritique.com/liste/Box_office_France_2005/1532876",
    "https://www.senscritique.com/liste/box_office_france_2006/1532886",
    "https://www.senscritique.com/liste/box_office_france_2007/1532899",
    "https://www.senscritique.com/liste/Box_office_France_2008/1532908",
    "https://www.senscritique.com/liste/box_office_france_2009/1532917",
    "https://www.senscritique.com/liste/box_office_france_2010/1532928",
    "https://www.senscritique.com/liste/box_office_france_2011/1532936",
    "https://www.senscritique.com/liste/Box_office_France_2012/1532947",
    "https://www.senscritique.com/liste/box_office_france_2013/1532958",
    "https://www.senscritique.com/liste/box_office_france_2014/1532966",
    "https://www.senscritique.com/liste/box_office_france_2015/765863",
    "https://www.senscritique.com/liste/box_office_france_2016/1169527",
    "https://www.senscritique.com/liste/le_box_office_france_2017/1641191",
    "https://www.senscritique.com/liste/le_box_office_france_2018/1971528",
    "https://www.senscritique.com/liste/le_box_office_france_2019/2300430",
    "https://www.senscritique.com/liste/le_box_office_france_2020/2574934",
    "https://www.senscritique.com/liste/le_box_office_france_2021/2996038",
    "https://www.senscritique.com/liste/le_box_office_france_2022/3159342",
    "https://www.senscritique.com/liste/le_box_office_france_2023/3370432",
    
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2000/2318072",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2001/2318333",
    "https://www.senscritique.com/liste/box_office_des_films_de_l_annee_2003/2318470",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2002/2318452",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2004/2318500",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2005/2318945",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2006/2319182",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2007/2319354",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2008/2319792",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2009/2319958",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2010/2320266",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2011/2323274",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2012/2324708",
    "https://www.senscritique.com/liste/Box_Office_des_films_francais_de_l_annee_2013/2326361",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2014/2327559",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2015/2328059",
    "https://www.senscritique.com/liste/Box_Office_des_films_francais_de_l_annee_2016/2330769",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2017/2330877",
    "https://www.senscritique.com/liste/Box_Office_des_films_francais_de_l_annee_2018/2331602",
    "https://www.senscritique.com/liste/box_office_des_films_francais_de_l_annee_2019/2584679"

]
    start_urls = []
    for base_url in base_urls:
        for page in range(1, 16):
            start_urls.append(f"{base_url}?page={page}")


        # rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)
        
        film_details = LinkExtractor(restrict_css='h3 > a')
        rule_film_details = Rule(film_details,
                                callback='parse_item',
                                follow=False,
                                )
    
    
    rules = (rule_film_details,)
    
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers={
                'User-Agent': self.user_agent
            })




    def parse_item(self, response):
        item = {}
        item["titre"] = response.xpath('//h1/text()').get()
        
        
        item["annee_1"] = response.xpath('//*[@id="__next"]/div[1]/div/main[1]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/p/text()').get()
        item["annee_2"] = response.xpath('//*[@id="__next"]/div[1]/div/main[1]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/p[2]/text()').get()
        
        item["acteur_1"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/a/text()').get()
        item["acteur_2"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div/a/text()').get()
        item["acteur_3"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div/div/a/text()').get()
        
        item["duree_1"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/text()[3]').get()
        item["duree_2"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/text()[2]').get()
        item["duree_3"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/text()[4]').get()
        
        item["sortie_1"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/text()[3]').get()
        item["sortie_2"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/text()[2]').get()
        item["sortie_3"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/text()[4]').get()
        item["sortie_4"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/text()[5]').get()


        item["realisateur"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[1]/p/a/span/span/text()').get()
        
        item["pays_1"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[4]/span/text()').get()
        item["pays_2"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div/div[2]/div[1]/div/div/span[3]/span/text()').get()

        item["genre_1"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[2]/a[1]/text()').get()
        item["genre_2"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[2]/a[2]/text()').get()
        item["genre_3"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[2]/a[3]/text()').get()
        
        item["note_film"] = response.xpath('//*[@id="__next"]/div[1]/div/main[1]/div/div[3]/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/text()').get()
        
        item["franchise_1"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[3]/a[1]/text()').get()
        item["franchise_2"] = response.xpath('//*[@id="__next"]/div[1]/div/main[2]/div/div[1]/div[2]/div[1]/div/div/span[3]/a[2]/text()').get()
        
        return item


run_spider()