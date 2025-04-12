# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
from time import sleep
import random

# Define a class to encapsulate Taobao login and data crawling functionalities
class taobao_infos:

    # Constructor to initialize necessary components
    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url

        options = webdriver.ChromeOptions()
        # Disable images to speed up the loading process
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # Set browser in developer mode to avoid detection by websites
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # Initialize Chrome WebDriver with specified options and path
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        # Initialize WebDriverWait with a timeout of 10 seconds
        self.wait = WebDriverWait(self.browser, 10)


    # Method to perform login action
    def login(self):
        # Open the login page
        self.browser.get(self.url)

        # Implicit wait until the password login option is present and click it
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="forget-pwd J_Quick2Static"]').click()

        # Implicit wait until the Weibo login option is present and click it
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="weibo-login"]').click()

        # Implicit wait until the Weibo username field is present and input the username
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('username').send_keys(weibo_username)

        # Implicit wait until the Weibo password field is present and input the password
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('password').send_keys(weibo_password)

        # Implicit wait until the submit button is present and click it
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()

        # Wait until the Taobao username is present (indicating successful login) and print it
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        print(taobao_name.text)


    # Method to simulate scrolling down the page
    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            # Simulate scrolling up and down based on the value of i
            if i % 2 == 0:
                js = "var q=document.documentElement.scrollTop=" + str(300 + 400 * i)
            else:
                js = "var q=document.documentElement.scrollTop=" + str(200 * i)
            self.browser.execute_script(js)
            sleep(0.1)

        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.1)


    # Method to crawl Taobao purchased items data
    def crawl_good_buy_data(self):
        # Navigate to the Taobao purchased items page
        self.browser.get("https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm")

        # Iterate through all pages
        for page in range(1, 1000):
            # Wait until all purchased items data on the page is loaded
            good_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tp-bought-root > div.js-order-container')))

            # Get the HTML source code of the page
            html = self.browser.page_source

            # Parse the HTML source code using pq module
            doc = pq(html)

            # Store the purchased items data on the current page
            good_items = doc('#tp-bought-root .js-order-container').items()

            # Iterate through all items on the page
            for item in good_items:
                good_time_and_id = item.find('.bought-wrapper-mod__head-info-cell___29cDO').text().replace('\n', "").replace('\r', "")
                good_merchant = item.find('.seller-mod__container___1w0Cx').text().replace('\n', "").replace('\r', "")
                good_name = item.find('.sol-mod__no-br___1PwLO').text().replace('\n', "").replace('\r', "")
                # Print the purchase time, order ID, merchant name, and item name
                print(good_time_and_id, good_merchant, good_name)

            print('\n\n')

            # Simulate scrolling down to mimic human browsing behavior
            swipe_time = random.randint(1, 3)
            self.swipe_down(swipe_time)

            # Wait until the next page button is present and click it
            next_page_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pagination-next')))
            next_page_button.click()
            sleep(2)


if __name__ == "__main__":
    # Before using, please read the usage instructions in README.MD
    chromedriver_path = "/Users/bird/Desktop/chromedriver.exe"  # Change to your chromedriver's full path address
    weibo_username = "Change to your Weibo username"  # Change to your Weibo username
    weibo_password = "Change to your Weibo password"  # Change to your Weibo password

    a = taobao_infos()
    a.login()  # Login
    a.crawl_good_buy_data()  # Crawl Taobao purchased items data
