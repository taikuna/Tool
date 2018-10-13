# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_driver, options = chrome_options)

driver.implicitly_wait(3)

driver.get("https://mail.google.com/mail/u/0/#inbox")
driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Gmail'])[3]/following::div[8]").click()
driver.find_element_by_id(":q3").send_keys("ti@gmail.com")
driver.find_element_by_id(":pl").send_keys("Test.Subject")
driver.find_element_by_id(":qq").click()
driver.find_element_by_id(":qq").click()
driver.find_element_by_id(":qq").send_keys("Test.Subject")
driver.find_element_by_id(":pb").click()
