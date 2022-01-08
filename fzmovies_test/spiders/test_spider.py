# -*- coding: utf-8 -*-
import scrapy


class TestSpiderSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['www.fzmovies.net']
    start_urls = ['http://www.fzmovies.net/']

    def parse(self, response):
        pass
