from selenium import webdriver
from selenium.webdriver.common.by import By

import time

from selenium import webdriver



driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.

driver.get('http://www.google.com/')

time.sleep(5) # Let the user actually see something!

search_box = driver.find_element_by_name('q')

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5) # Let the user actually see something!

driver.quit()


driver = webdriver.Chrome("C:/Program Files/chromedriver/chromedriver")
f = open("G://data/jobkorea_link.txt",'w')

for i in range(1,369):
        driver.get("https://www.jobkorea.co.kr/starter/passassay?schTxt=&Page="+str(i)) 
        # page에 따른 경로
        paper_list = driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[2]/div[5]/ul")
        # 자기소개서 목록을 담아놓은 태그
        driver.implicitly_wait(3)
        urls = paper_list.find_elements(By.TAG_NAME,'a') # 거기에서 a태그만 가져온다
        for url in urls:
            if 'selfintroduction' in url.get_attribute('href'): 
            #가끔씩 이상한 경로가 섞여들어와서 제외하고 진행했다.
                pass
            else:
                array.append(url.get_attribute('href')) # href안에 있는 경로를 array에 추가해준다.
        array = list(set(array))
for content in array: # array를 파일에 저장해준다
        f.write(content+'\n') 