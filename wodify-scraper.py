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

        #self.driver.save_screenshot('screenshot.png')

    def select_reports_tab(self):
        elem = self.driver.find_element_by_xpath("//div/a/span[text()='Reports']")
        elem = elem.find_element_by_xpath('..')
        elem.click()

        def reports_loaded(driver):
            elem = self.driver.find_element_by_xpath("//div/a/span[text()='Reports']")
            parent_div = elem.find_element_by_xpath('../..')
            return 'Menu_TopMenuActive' in parent_div.get_attribute('class')

        wait = WebDriverWait(self.driver, 10)
        wait.until(reports_loaded)

        #self.driver.save_screenshot('screenshot.png')

    def select_performance_results(self):
        elem = self.driver.find_element_by_xpath("//div/a[text()='Performance Results']")
        elem.click()

        def reports_loaded(driver):
            path = "//div/a/span[text()='Performance Results: Weightlifting']"
            try:
                elem = self.driver.find_element_by_xpath(path)
                return elem.is_displayed()
            except NoSuchElementException:
                return False

        wait = WebDriverWait(self.driver, 10)
        wait.until(reports_loaded)

        self.driver.save_screenshot('screenshot.png')
        
    def select_performance_results_weightlifting(self):
        path = "//div/a/span[text()='Performance Results: Weightlifting']"
        elem = self.driver.find_element_by_xpath(path)
        elem = elem.find_element_by_xpath('..')
        elem.click()
        
    def scrape(self):
        self.driver.get(self.url)
        self.login()
        self.switch_to_wodify_admin()
        self.select_reports_tab()
        self.select_performance_results()
        self.select_performance_results_weightlifting()

if __name__ == '__main__':
    scraper = WodifyScraper()
    scraper.scrape()
