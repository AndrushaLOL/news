# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from news.items import News
from news.utils import CleanText


class RiaSpider(scrapy.Spider):
    urls = {
        'politics': 'http://ria.ru/services/politics/more.html?id=1547985429&date=20181214T131501',
        'society': 'http://ria.ru/services/society/more.html?id=1548005108&date=20181214T170400',
        'world': 'http://ria.ru/services/world/more.html?id=1548006110&date=20181214T171920',
        'science': 'http://ria.ru/services/science/more.html?id=1547967537&date=20181214T082615',
        'culture': 'http://ria.ru/services/culture/more.html?id=1547952810&date=20181213T185932',
        'religion': 'http://ria.ru/services/religion/more.html?id=1547937808&date=20181213T155344'
    }

    name = 'ria'
    allowed_domains = ['ria.ru']
    start_urls = ['http://ria.ru/']

    XPATH_TO_TITLE = '//*[@id="endless"]/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/h1/text()'

    normalizer = CleanText()

    def start_requests(self):
        for tag in self.urls.keys():
            req = scrapy.Request(url=self.urls[tag], callback=self.parse)
            req.meta['label'] = tag
            req.meta['depth'] = 1
            yield req

    def parse(self, response):
        next_link = response.css('.list-items-loaded::attr(data-next-url)').extract_first()
        print(next_link)
        links = LinkExtractor(allow=r'/\d*/').extract_links(response)
        for link in links:
            req = scrapy.Request(url=link.url, callback=self.parse_news)
            req.meta['label'] = response.meta['label']
            yield req
        # if response.meta['depth'] < 5:
        req = scrapy.Request(url=urljoin(self.start_urls[0], next_link), callback=self.parse)
        req.meta['depth'] = response.meta['depth'] + 1
        req.meta['label'] = response.meta['label']
        yield req

    def parse_news(self, response):
        print(response.url)

        title = response.xpath(self.XPATH_TO_TITLE).extract_first()
        text = ' '.join(response.css('.article__text::text').extract())

        text = self.normalizer.clean_text(text)
        title = self.normalizer.clean_text(title)

        news = News()
        news['label'] = response.meta['label']
        news['title'] = title
        news['text'] = text
        news['url'] = response.url

        if text:
            yield news
