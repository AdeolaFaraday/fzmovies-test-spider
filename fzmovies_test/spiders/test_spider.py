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

    def parse(self, response):
        # img = response.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        movie_name = 'life itself'
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
            yield response.follow(url=film_link.get_attribute('href'), callback=self.parse_film, meta={'film': film_link.get_attribute('href')})

    def parse_film(self, response):
        link = response.request.meta['film']
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_path = which("chromedriver")
        driver = webdriver.Chrome(
            executable_path=chrome_path, options=chrome_options)

        driver.get(link)

        movie_title = driver.find_element_by_xpath(
            "//div[@class='moviename']").get_attribute("textContent")
        movie_size = driver.find_element_by_xpath(
            "(//dcounter)[4]").get_attribute("innerHTML")
        movie_img = driver.find_element_by_xpath(
            "//img[@itemprop='image']").get_attribute('src')
        button = driver.find_element_by_xpath(
            "//a[@id='downloadoptionslink2']")
        driver.execute_script("arguments[0].click();", button)

        button_2 = driver.find_element_by_xpath("//a[@id='downloadlink']")
        driver.execute_script("arguments[0].click();", button_2)

        download_link = driver.find_element_by_xpath(
            "//ul[@class='downloadlinks']/p[1]/input").get_attribute('value')
        yield {
            'movie_title': movie_title,
            'movie_size': movie_size,
            'movie_img': movie_img,
            'movie_download_link': download_link
        }
