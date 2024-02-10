import scrapy

class MySpider(scrapy.Spider):
    name = 'spooder'

    def start_requests(self):
        search_urls = [
            'http://example.com/search?query=your_search_query',
        ]
        for url in search_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
        pass
