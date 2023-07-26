# # # import scrapy

# # # class MoviesSpider(scrapy.Spider):
# # #     name = 'movies_spider'
# # #     allowed_domains = ['allocine.fr']
# # #     start_urls = ['https://www.allocine.fr/films/?page=1']

# # #     def parse(self, response):
# # #         for movie in response.css('a.meta-title-link'):
# # #             title = movie.css('::text').get().strip()
# # #             link = movie.attrib['href']
# # #             full_link = self.get_full_link(link)
# # #             yield scrapy.Request(full_link, callback=self.parse_movie_page, meta={'title': title})

# # #         next_page = response.css('a[data-page-number]::attr(href)').get()
# # #         if next_page:
# # #             yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

# # #     def parse_movie_page(self, response):
# # #         title = response.meta['title']
# # #         entrees_element = response.css('td[data-heading="Entrées"]::text').get()
# # #         if entrees_element:
# # #             entrees = entrees_element.strip()
# # #         else:
# # #             entrees = "Informations sur les entrées non trouvées"
        
# # #         yield {
# # #             'Titre': title,
# # #             'Entrées': entrees
# # #         }

# # #     def get_full_link(self, rel_link):
# # #         base_url = 'https://www.allocine.fr'
# # #         return base_url + rel_link.replace('fichefilm_gen_cfilm=', 'fichefilm-').replace('.html', '/box-office/')


# # import scrapy

# # class MoviesSpider(scrapy.Spider):
# #     name = 'movies_spider'
# #     allowed_domains = ['allocine.fr']

# #     def start_requests(self):
# #         base_url = 'https://www.allocine.fr/films/?page={}'
# #         # Boucle pour parcourir les pages de 1 à 7693
# #         for page_number in range(1, 7694):
# #             url = base_url.format(page_number)
# #             yield scrapy.Request(url, self.parse)

# #     def parse(self, response):
# #         for movie in response.css('a.meta-title-link'):
# #             title = movie.css('::text').get().strip()
# #             link = movie.attrib['href']
# #             full_link = self.get_full_link(link)
# #             yield scrapy.Request(full_link, callback=self.parse_movie_page, meta={'title': title})

# #     def parse_movie_page(self, response):
# #         title = response.meta['title']
# #         entrees_element = response.css('td[data-heading="Entrées"]::text').get()
# #         if entrees_element:
# #             entrees = entrees_element.strip()
# #         else:
# #             entrees = "Informations sur les entrées non trouvées"
        
# #         yield {
# #             'Titre': title,
# #             'Entrées': entrees
# #         }

# #     def get_full_link(self, rel_link):
# #         base_url = 'https://www.allocine.fr'
# #         return base_url + rel_link.replace('fichefilm_gen_cfilm=', 'fichefilm-').replace('.html', '/box-office/')


# import scrapy

# class MoviesSpider(scrapy.Spider):
#     name = 'movies_spider'
#     allowed_domains = ['allocine.fr']

#     def start_requests(self):
#         base_url = 'https://www.allocine.fr/films/?page={}'
#         # Boucle pour parcourir les pages de 1 à 7693
#         for page_number in range(1, 7694):
#             url = base_url.format(page_number)
#             yield scrapy.Request(url, self.parse)

#     def parse(self, response):
#         for movie in response.css('a.meta-title-link'):
#             title = movie.css('::text').get().strip()
#             link = movie.attrib['href']
#             full_link = self.get_full_link(link)
#             yield scrapy.Request(full_link, callback=self.parse_movie_page, meta={'title': title})

#     def parse_movie_page(self, response):
#         title = response.meta['title']
#         entrees_elements = response.css('td[data-heading="Entrées"]::text').getall()[:2]  # Get the first two elements
#         entrees = [entree.strip() for entree in entrees_elements]

#         yield {
#             'Titre': title,
#             'Entrées': entrees
#         }

#     def get_full_link(self, rel_link):
#         base_url = 'https://www.allocine.fr'
#         return base_url + rel_link.replace('fichefilm_gen_cfilm=', 'fichefilm-').replace('.html', '/box-office/')

import scrapy

class MoviesSpider(scrapy.Spider):
    name = 'moviesspider'
    allowed_domains = ['allocine.fr']

    def start_requests(self):
        base_url = 'https://www.allocine.fr/films/?page={}'
        # Boucle pour parcourir les pages de 1 à 7693
        for page_number in range(1, 7694):
            url = base_url.format(page_number)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for movie in response.css('a.meta-title-link'):
            title = movie.css('::text').get().strip()
            link = movie.attrib['href']
            full_link = self.get_full_link(link)
            yield scrapy.Request(full_link, callback=self.parse_movie_page, meta={'title': title})

    def parse_movie_page(self, response):
        title = response.meta['title']

        # Vérifier si la section "Box Office France" existe
        box_office_france = response.css('h2:contains("Box Office France")').get()
        if box_office_france:
            entrees_elements = response.css('td[data-heading="Entrées"]::text').getall()[:2]  # Get the first two elements
            entrees = [entree.strip() for entree in entrees_elements]

            yield {
                'Titre': title,
                'Entrées': entrees
            }

    def get_full_link(self, rel_link):
        base_url = 'https://www.allocine.fr'
        return base_url + rel_link.replace('fichefilm_gen_cfilm=', 'fichefilm-').replace('.html', '/box-office/')
