import scrapy

class MySpider(scrapy.Spider):
    name = 'spooder'

    def start_requests(self):
        search_urls = [
            'https://search.espncricinfo.com/ci/content/site/search.html?search=dhoni;type=player',
        ]
        for url in search_urls:
            yield scrapy.Request(url=url, headers={'user-agent': 'Mozilla/5.0'}, callback=self.parse)

    def parse(self, response):
        for result in response.css('ul.search-results li'):
            yield {
                'player':result.css('p::text').get().split(',')[0],
                'profile':result.css('a::attr(href)').get()
            }