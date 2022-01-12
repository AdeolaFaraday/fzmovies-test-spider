# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which
from scrapy_selenium import SeleniumRequest


class TestSpiderSpider(scrapy.Spider):
    name = 'test_fzmovies'
    allowed_domains = ['www.fzmovies.net']
    start_urls = ['http://www.fzmovies.net/']

    # def start_requests(self):
    #     yield SeleniumRequest(
    #         url='http://www.fzmovies.net/',
    #         wait_time=3,
    #         screenshot=True,
    #         callback=self.parse
    #     )
    def __init__(self, name=None, *args, **kwargs):
        super(TestSpiderSpider, self).__init__(*args, **kwargs)
        self.movie_name = name

    def parse(self, response):
        # img = response.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        print(self.movie_name, "self.movie_nameself.movie_nameself.movie_nameself.movie_nameself.movie_nameself.movie_name")
        movie_name = self.movie_name
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_path = which("chromedriver")
        driver = webdriver.Chrome(
            executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.fzmovies.net/")

        obj = driver.switch_to.alert

        # Retrieve the message on the Alert window
        obj.text

        # time.sleep(2)

        # Or Dismiss the Alert using
        obj.dismiss()

        search_input = driver.find_element_by_xpath(
            "//input[@id='searchname']")

        # print("shows following message: " + search_input)
        search_input.send_keys(movie_name)

        search_input.send_keys(Keys.ENTER)

        # time.sleep(2)

        film_links = driver.find_elements_by_xpath(
            "//div[@class='mainbox']/table/tbody/tr/td[2]/span/a")
        # print('attribute here', film_link.get_attribute('href'))
        # print('film_link' + film_link)
        # # rur_tab[4].click()
        print(film_links, 'FILM LINK HEREEEEEEEEEEEEEEE')
        for film_link in film_links:
            # yield {
            #     'film': film_link.get_attribute('href')
            # }
            yield response.follow(url=film_link.get_attribute('href'), callback=self.parse_film, meta={'film': film_link.get_attribute('href')})

    def parse_film(self, response):
        yield response.follow(url=response.xpath("//a[@id='downloadoptionslink2']//@href")[1].get(), callback=self.parse_first_link,
                              meta={'movie_title': response.xpath("//div[@class='moviename']//text()").get(), 'movie_size': response.xpath("(//dcounter)[4]//text()").get(),
                                    'movie_img': response.xpath("//img[@itemprop='image']//@src").get()
                                    }
                              )

    def parse_first_link(self, response):
        yield response.follow(url=response.xpath("//a[@id='downloadlink']//@href").get(), callback=self.parse_second_link, meta={'movie_title': response.request.meta['movie_title'], 'movie_size': response.request.meta['movie_size'],
                                                                                                                                 'movie_img': response.request.meta['movie_img']
                                                                                                                                 })

    def parse_second_link(self, response):
        yield {
            'movie_title': response.request.meta['movie_title'],
            'movie_size': response.request.meta['movie_size'],
            'movie_img': response.request.meta['movie_img'],
            'download_link': response.xpath("//a[@id='dlink0']//@href").get()
        }

# http://localhost:9080/crawl.json?spider_name=test_fzmovies&&start_requests=True&&crawl_args={"name":"clouds"}