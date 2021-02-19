import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from eekch.items import Article


class EekSpider(scrapy.Spider):
    name = 'eek'
    start_urls = ['https://www.eek.ch/aktuell/news/']

    def parse(self, response):
        links = response.xpath('//div[@class="article articletype-0"]//h3/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h3[@itemprop="headline"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//time/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d.%m.%Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@itemprop="articleBody"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        # author = response.xpath('').get()
        #
        # category = response.xpath('').get()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        # item.add_value('author', author)
        # item.add_value('category', category)

        return item.load_item()
