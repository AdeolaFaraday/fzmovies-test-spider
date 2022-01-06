# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which
from scrapy_selenium import SeleniumRequest


class FzmoviesSpider(scrapy.Spider):
    name = 'fzmovies'
    # allowed_domains = ['www.fzmovies.net']
    # start_urls = ['http://www.fzmovies.net/']

    def start_requests(self):
        yield SeleniumRequest(
            url='http://www.fzmovies.net/',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        # img = response.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.fzmovies.net/")

        obj = driver.switch_to.alert

        # Retrieve the message on the Alert window
        message = obj.text

        print("shows following message: " + message)

        time.sleep(2)

        # Or Dismiss the Alert using
        obj.dismiss()

        search_input = driver.find_element_by_xpath(
            "//input[@id='searchname']")

        # print("shows following message: " + search_input)
        search_input.send_keys("I still believe")

        search_input.send_keys(Keys.ENTER)


        yield {
            'result': message
        }
