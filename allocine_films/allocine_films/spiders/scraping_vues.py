import scrapy

class MoviesSpider(scrapy.Spider):
    name = 'vuesspider'
    allowed_domains = ['allocine.fr']

    def start_requests(self):
        base_url = 'https://www.allocine.fr/films/?page={}'
        # Loop to iterate through pages from 1 to 2 (for testing)
        for page_number in range(1, 2):
            url = base_url.format(page_number)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for movie in response.css('a.meta-title-link'):
            title = movie.css('::text').get().strip()

            # Extracting video link
            video_link = movie.xpath('.//a[contains(concat(" ", @class, " "), " thumbnail-container ") and contains(concat(" ", @class, " "), " thumbnail-link ")]/@href').get()

            # video_link = movie.xpath('.//a[contains(@class, "thumbnail-container thumbnail-link")]/@href').get()
            if video_link:
                yield scrapy.Request(video_link, callback=self.parse_movie_page, meta={'title': title})
            print('lalalalalalalallallalalallalallalalall LALALALLLALALLALALALALALAL',  video_link, title)

    def parse_movie_page(self, response):
        title = response.meta['title']

        # Extracting views
        views_text = response.css('div.media-info-item.icon.icon-eye::text').get()
        if views_text:
            views = views_text.split()[0]  # Extract the number from "31 251 vues"
        else:
            views = 'N/A'
        print('mimmimimmimimimimimmimimimmimimimmimimi', views)
        
        yield {
            'Titre': title,
            'Vues': views
        }
