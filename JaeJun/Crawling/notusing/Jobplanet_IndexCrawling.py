import time
from webdriver_manager.chrome import ChromeDriverManager # 크롬 드라이버 자동 업데이트
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pyautogui




driver = webdriver.Chrome()

driver.get(url = 'https://www.jobplanet.co.kr/job')
time.sleep(5)

driver.find_element(By.ID, 'search_bar_search_query').send_keys('삼성전자')
time.sleep(1)
pyautogui.press('enter')

companies = driver.find_element(By.CLASS_NAME, 'is_company_card').find_elements(By.CLASS_NAME, 'result_card')

for company in companies:
    title = company.find_elements(By.TAG_NAME, 'a')[-1].text
    url = company.find_elements(By.TAG_NAME, 'a')[-1].get_attribute('href')
    companyCode = url.split('/')[4]
    print(f'회사명 : {title} 회사코드 : {companyCode}')
    driver.get(url)
    input()