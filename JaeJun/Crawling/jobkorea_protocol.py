# jobkorea_protocol.py

import jobkorea_userPortfolio
from selenium import webdriver
from selenium.webdriver.common.by import By

jobkorea_userPortfolio.link_crawl

file = open('C://data/jobkorea_link.txt','r')
driver = webdriver.Chrome("C:/Program Files/chromedriver/chromedriver")
jobkorea_userPortfolio.login_protocol(driver=driver)
while True: # 7354개
    file_url = file.readline()
    if file_url == "":
        break
    jobkorea_userPortfolio.self_introduction_crawl(driver=driver,file_url=file_url)