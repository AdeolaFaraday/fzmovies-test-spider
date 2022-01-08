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
    allowed_domains = ['www.fzmovies.net']
    start_urls = ['http://www.fzmovies.net/']

    # def start_requests(self):
    #     yield SeleniumRequest(
    #         url='http://www.fzmovies.net/',
    #         wait_time=3,
    #         screenshot=True,
    #         callback=self.parse
    #     )

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
        obj.text

        time.sleep(2)

        # Or Dismiss the Alert using
        obj.dismiss()

        search_input = driver.find_element_by_xpath(
            "//input[@id='searchname']")

        # print("shows following message: " + search_input)
        search_input.send_keys("I still believe")

        search_input.send_keys(Keys.ENTER)

        # time.sleep(2)

        film_link = driver.find_element_by_xpath(
            "//div[@class='mainbox']/table/tbody/tr/td[2]/span/a")
        # print('attribute here', film_link.get_attribute('href'))
        # print('film_link' + film_link)
        # # rur_tab[4].click()
        film_link.click()

        # time.sleep(2)

        # download_follow_link = driver.find_element_by_xpath("//a[@id='downloadoptionslink2']")

        button = driver.find_element_by_xpath(
            "//a[@id='downloadoptionslink2']")
        driver.execute_script("arguments[0].click();", button)

        button = driver.find_element_by_xpath("//a[@id='downloadlink']")
        driver.execute_script("arguments[0].click();", button)

        download_link = driver.find_element_by_xpath(
            "//ul[@class='downloadlinks']/p[1]/input").get_attribute('value')
        print(download_link)
        print('PAGE SOURCE BOLDLY WRITTEN HERE')
        self.html = driver.page_source
        driver.close()
        yield {
            'movie_download_link': download_link
        }
