import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = 'restaurants'
    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Restaurants-g303506-Rio_de_Janeiro_State_of_Rio_de_Janeiro.html']
    headers = {
        "User-Agent": "PostmanRuntime/7.32.2"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        links = response.xpath('//*[@id="component_2"]/div/div/div/div[1]/div[2]/div[1]/div/span/a/@href')
        for link in links:
            yield {
                'link': link.get()
            }

        next_page = response.xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a/@href')
        if next_page:
            yield scrapy.Request(response.urljoin(next_page[0].get()), headers=self.headers)
