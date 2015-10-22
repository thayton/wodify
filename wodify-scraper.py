#!/usr/bin/env python

import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

class WodifyScraper(object):
    def __init__(self):
        self.url = 'http://login.wodify.com'
        self.username = 'nighthawk'
        self.password = 'wodifyhell'
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def login(self):
        username_elem = self.driver.find_element_by_id('wt73_wtMainContent_wtUserNameInput')
        password_elem = self.driver.find_element_by_id('wt73_wtMainContent_wtPasswordInput')

        username_elem.send_keys(self.username)
        password_elem.send_keys(self.password)
        
        login_elem = self.driver.find_element_by_id('wt73_wtMainContent_wt59')
        login_elem.click()

        def logged_in(driver):
            try:
                elem = driver.find_element_by_link_text('WOD')
                return elem.is_displayed()
            except NoSuchElementException:
                return False

        wait = WebDriverWait(self.driver, 10)
        wait.until(logged_in)

        #self.driver.save_screenshot('screenshot.png')

    def switch_to_wodify_admin(self):
        s = BeautifulSoup(self.driver.page_source, 'html.parser')
        r = re.compile(r'^W_Theme_UI_wt\d+_block_wt\d_wtApplications$')
        e = s.find(id=r)

        elem = self.driver.find_element_by_id(e['id'])
        text = 'Wodify Admin'

        Select(elem).select_by_visible_text(text)

        def admin_page_loaded(driver):
            s = BeautifulSoup(driver.page_source, 'html.parser')
            r = re.compile(r'^W_Theme_UI_wt\d+_block_wt\d_wtApplications$')
            e = s.find(id=r)

            elem = self.driver.find_element_by_id(e['id'])
            text = 'Wodify Admin'

            return Select(elem).first_selected_option.text == text

        wait = WebDriverWait(self.driver, 10)
        wait.until(admin_page_loaded)

        self.driver.save_screenshot('screenshot.png')

    def scrape(self):
        self.driver.get(self.url)
        self.login()
        self.switch_to_wodify_admin()

if __name__ == '__main__':
    scraper = WodifyScraper()
    scraper.scrape()
