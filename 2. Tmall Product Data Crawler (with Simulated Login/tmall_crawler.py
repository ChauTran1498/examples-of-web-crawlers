# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
from time import sleep

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


    # Delay operation with an optional alert message
    def sleep_and_alert(self, sec, message, is_alert):
        for second in range(sec):
            if is_alert:
                alert = "alert(\"" + message + ":" + str(sec - second) + " seconds\")"
                self.browser.execute_script(alert)
                al = self.browser.switch_to.alert
                sleep(1)
                al.accept()
            else:
                sleep(1)


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


    # Method to get the total number of pages of Tmall products
    def search_toal_page(self):
        # Wait until all Tmall product data on the page is loaded
        good_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList > div.product > div.product-iWrap')))

        # Get the total number of pages of Tmall products
        number_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form')))
        page_total = number_total.text.replace("共", "").replace("页，到第页 确定", "").replace("，", "")

        return page_total


    # Method to navigate to the next page
    def next_page(self, page_number):
        # Wait until the input field for page number is present
        input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > input.ui-page-skipTo')))

        # Wait until the submit button is present
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > button.ui-btn-s')))

        # Clear the current page number
        input.clear()

        # Enter the new page number
        input.send_keys(page_number)

        # Force a delay of 1 second to avoid being detected as a bot
        sleep(1)

        # Click the submit button
        submit.click()


    # Method to simulate scrolling down the page
    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
            self.browser.execute_script(js)
            sleep(0.1)
        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.2)


    # Method to crawl Tmall product data
    def crawl_good_data(self):
        # Navigate to the Tmall search page for badminton rackets
        self.browser.get("https://list.tmall.com/search_product.htm?q=羽毛球")
        err1 = self.browser.find_element_by_xpath("//*[@id='content']/div/div[2]").text
        err1 = err1[:5]
        if err1 == "喵~没找到":
            print("No results found")
            return
        try:
            self.browser.find_element_by_xpath("//*[@id='J_ComboRec']/div[1]")
            err2 = self.browser.find_element_by_xpath("//*[@id='J_ComboRec']/div[1]").text
            err2 = err2[:5]
            if err2 == "我们还为您":
                print("Too few items to query")
                return
        except:
            print("Can crawl these items")

        # Get the total number of pages of Tmall products
        page_total = self.search_toal_page()
        print("Total pages: " + page_total)

        # Iterate through all pages
        for page in range(2, int(page_total)):
            # Wait until all product data on the page is loaded
            good_total = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList > div.product > div.product-iWrap')))

            # Wait until the input field for page number is present
            input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page > div.ui-page-wrap > b.ui-page-skip > form > input.ui-page-skipTo')))

            # Get the current page number
            now_page = input.get_attribute('value')
            print("Current page: " + now_page + ", Total pages: " + page_total)

            # Get the HTML source code of the page
            html = self.browser.page_source

            # Parse the HTML source code using pq module
            doc = pq(html)

            # Store Tmall product data
            good_items = doc('#J_ItemList .product').items()

            # Iterate through all products on the page
            for item in good_items:
                good_title = item.find('.productTitle').text().replace('\n', "").replace('\r', "")
                good_status = item.find('.productStatus').text().replace(" ", "").replace("笔", "").replace('\n', "").replace('\r', "")
                good_price = item.find('.productPrice').text().replace("¥", "").replace(" ", "").replace('\n', "").replace('\r', "")
                good_url = item.find('.productImg').attr('href')
                print(good_title + "   " + good_status + "   " + good_price + "   " + good_url + '\n')

            # Simulate scrolling down to mimic human browsing behavior
            self.swipe_down(2)

            # Navigate to the next page
            self.next_page(page)

            # Wait for the sliding verification code to appear, timeout is 5 seconds, check every 0.5 seconds
            # Most of the time, the sliding verification code will not appear, so this can be commented out if needed
            # sleep(5)
            try:
                WebDriverWait(self.browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, "nc_1_n1z")))  # Wait for the sliding control to appear
                swipe_button = self.browser.find_element_by_id('nc_1_n1z')  # Get the sliding control

                # Simulate dragging the slider
                action = ActionChains(self.browser)  # Instantiate an ActionChains object
                action.click_and_hold(swipe_button).perform()  # Perform the stored actions
                action.reset_actions()
                action.move_by_offset(580, 0).perform()  # Move the slider
            except Exception as e:
                print('Failed to get button: ', e)


if __name__ == "__main__":
    # Before using, please read the usage instructions in README.MD
    chromedriver_path = "/Users/bird/Desktop/chromedriver.exe"  # Change to your chromedriver's full path address
    weibo_username = "Change to your Weibo username"  # Change to your Weibo username
    weibo_password = "Change to your Weibo password"  # Change to your Weibo password

    a = taobao_infos()
    a.login()  # Login
    a.crawl_good_data()  # Crawl Tmall product data
