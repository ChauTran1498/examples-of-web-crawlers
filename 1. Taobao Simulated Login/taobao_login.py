# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define a class to encapsulate Taobao login functionalities
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

        # Wait until the password login option is present and click it
        password_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        # Wait until the Weibo login option is present and click it
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        # Wait until the Weibo username field is present and input the username
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        weibo_user.send_keys(weibo_username)

        # Wait until the Weibo password field is present and input the password
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.send_keys(weibo_password)

        # Wait until the submit button is present and click it
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()

        # Wait until the Taobao username is present (indicating successful login) and print it
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        print(taobao_name.text)




# Usage instructions:
# 1. Download Chrome browser from https://www.google.com/chrome/
# 2. Check your Chrome version and download corresponding chromedriver from http://chromedriver.storage.googleapis.com/index.html
# 3. Specify the absolute path of chromedriver
# 4. Install Selenium using pip install selenium
# 5. Bind Taobao account with Weibo at https://account.weibo.com/set/bindsns/bindtaobao

if __name__ == "__main__":


    chromedriver_path = "/Users/bird/Desktop/chromedriver.exe" # Replace with your actual chromedriver path
    weibo_username = "Replace with your Weibo username" # Replace with your actual Weibo username
    weibo_password = "Replace with your Weibo password" # Replace with your actual Weibo password

    a = taobao_infos()
    a.login() # Execute login
