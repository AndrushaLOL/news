# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from news.items import News
from news.utils import CleanText


class RiaSpider(scrapy.Spider):
    urls = {
        'politics': 'http://ria.ru/services/politics/more.html',
        'society': 'http://ria.ru/services/society/more.html',
        'world': 'http://ria.ru/services/world/more.html',
        'science': 'http://ria.ru/services/science/more.html',
        'culture': 'http://ria.ru/services/culture/more.html',
        'religion': 'http://ria.ru/services/religion/more.html',
        'economy': 'ttp://ria.ru/services/economy/more.html'
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

        news_raw = News()
        news_raw['label'] = response.meta['label']
        news_raw['title'] = title
        news_raw['text'] = text
        news_raw['url'] = response.url

        text = self.normalizer.clean_text(text)
        title = self.normalizer.clean_text(title)

        news_clean = News()
        news_clean['label'] = response.meta['label']
        news_clean['title'] = title
        news_clean['text'] = text
        news_clean['url'] = response.url

        if text:
            yield {
                'raw': news_raw,
                'clean': news_clean
            }
