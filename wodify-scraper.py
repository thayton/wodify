#!/usr/bin/env python

import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

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
            path = "//div/a/span[text()='Reports']"
            try:
                elem = self.driver.find_element_by_xpath(path)
                return elem.is_displayed()
            except:
                return False

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

        def performance_results_loaded(driver):
            path = "//td/a/span[text()='Performance Results: Weightlifting']"
            try:
                elem = self.driver.find_element_by_xpath(path)
                return elem.is_displayed()
            except NoSuchElementException:
                return False

        wait = WebDriverWait(self.driver, 10)
        wait.until(performance_results_loaded)

#        self.driver.save_screenshot('screenshot.png')
        
    def select_performance_results_weightlifting(self):
        path = "//td/a/span[text()='Performance Results: Weightlifting']"
        elem = self.driver.find_element_by_xpath(path)
        elem = elem.find_element_by_xpath('..')
        elem.click()

        def weightlifting_results_loaded(driver):
            path = "//div[@class='filter_Wrapper']"
            try:
                elem = self.driver.find_element_by_xpath(path)
                return elem.is_displayed()
            except NoSuchElementException:
                return False

        wait = WebDriverWait(self.driver, 10)
        wait.until(weightlifting_results_loaded)

        #self.driver.save_screenshot('screenshot.png')

    def select_date_all_time(self):
        path = "//div/select[contains(@id, 'block_wtcbDateRange')]"
        elem = self.driver.find_element_by_xpath(path)
        text = 'All Time'

        Select(elem).select_by_visible_text(text)

        def all_times_loaded(driver):
            isactive = driver.execute_script('return outsystems.internal.$.active;')
            return isactive == 0
            
        wait = WebDriverWait(self.driver, 20)
        wait.until(all_times_loaded)

        #self.driver.save_screenshot('screenshot.png')

    def scrape(self):
        self.driver.get(self.url)
        self.login()
        self.switch_to_wodify_admin()
        self.select_reports_tab()
        self.select_performance_results()
        self.select_performance_results_weightlifting()
        self.select_date_all_time()
        self.select_back_squat_component()
        print

if __name__ == '__main__':
    scraper = WodifyScraper()
    scraper.scrape()
