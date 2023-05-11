import scrapy
from scrapy.selector import Selector
import pymongo


class MySpider(scrapy.Spider):
    name = "anp"

    def start_requests(self):
        base_url = 'https://www.gov.br/anp/pt-br/canais_atendimento/imprensa/noticias-comunicados?b_start:int={}'
        page_numbers = range(0, 100, 20)  # generate page numbers from 0 to 80, incrementing by 20
        urls = [base_url.format(p) for p in page_numbers]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        links = selector.xpath('//*[@id="ultimas-noticias"]/ul/li/div/h2/a/@href')
        for link in links:
            yield scrapy.Request(url=response.urljoin(link.extract()), callback=self.parse_link)

    def parse_link(self, response):
        selector = Selector(response)
        p_texts = selector.xpath(
            '//*[@id="parent-fieldname-text"]/div/p/text() | //*[@id="parent-fieldname-text"]/div/p/a/text()')
        text = ' '.join(p_texts.getall())
        yield {
            'url': response.url,]
        
            'text': text,
        }

        # Connect to MongoDB and insert the scraped data
        client = pymongo.MongoClient("mongodb+srv://bayout:Ninamendes1%40@cluster0.bo6zstp.mongodb.net/test")
        db = client["compliance"]
        collection = db["compliance"]
        news = {
            'url': response.url,
            'text': text,
        }
        collection.insert_one(news)
        client.close()
