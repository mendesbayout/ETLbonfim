import scrapy
from scrapy.selector import Selector
import pymongo


class MySpider(scrapy.Spider):
    name = "sus"

    def start_requests(self):
        base_url = 'https://datasus.saude.gov.br/categoria/noticias/'
        page_numbers = range(1, 2)  # generate page numbers from 1 to 5
        urls = [base_url.format(p) for p in page_numbers]
        yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        links = selector.xpath('//h2[@class="entry-title"]/a/@href')
        for link in links:
            yield scrapy.Request(url=response.urljoin(link.extract()), callback=self.parse_link)

    def parse_link(self, response):
        selector = Selector(response)
        p_texts = selector.xpath('//div[@class="entry-content"]/p')
        text = ' '.join(p_texts.xpath('string()').extract())
        yield {
            'url': response.url,
            'text': text,
        }

        # Connect to MongoDB and insert the scraped data
        client = pymongo.MongoClient("<your-mongodb-connection-string>")
        db = client["complianceRAW"]
        collection = db["sus"]
        news = {
            'url': response.url,
            'text': text,
        }
        collection.insert_one(news)
        client.close()