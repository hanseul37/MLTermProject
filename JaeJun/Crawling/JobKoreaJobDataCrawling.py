import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs   
import time
import datetime
from tqdm import trange

# initialize url for crawling target web, and make it can change page number with f-string
page_no = 1
# url = f"https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D&tabType=recruit&Page_No={page_no}" # Query with keyword "데이터 분석"
url = f"https://www.jobkorea.co.kr/Search/?local=I000%2CB000%2CK000%2CG000%2C1000%2CO000%2CP000%2CE000%2CL000%2CM000%2CF000%2CD000%2CH000%2CJ000%2CC000%2CA000%2CN000%2CQ000&tabType=recruit&Page_No={page_no}" # query with searching in all region

# DataFrame 
df = pd.DataFrame( columns = ['회사명','공고명','채용 형태(경력, 신입)','학력','직장 위치','키워드','마감 기한','공고 링크'])

# Find out the total number of pages for crawling web-site

URLindex = 0
URLindex = URLindex + 1
response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
response.encoding = 'cp949'
soup = bs(response.text,'html.parser')
pages = soup.find('p','filter-text').find('strong').text.replace(',','')

# change page using outer for
# search 20 announcements per page using inner for
#  
for i in trange(int(pages)):                      
    url = f"https://www.jobkorea.co.kr/Search/?local=I000%2CB000%2CK000%2CG000%2C1000%2CO000%2CP000%2CE000%2CL000%2CM000%2CF000%2CD000%2CH000%2CJ000%2CC000%2CA000%2CN000%2CQ000&tabType=recruit&Page_No={page_no}"

    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    soup = bs(response.text,'html.parser')
    
    # find keywords in page data
    company_name = soup.find_all('a','name dev_view')
    exp = soup.find_all('span','exp')
    edu = soup.find_all('span','edu')
    loc = soup.find_all('span','loc long')
    date = soup.find_all('span','date')
    etc = soup.find_all('p','etc')
    info = soup.find_all('a','title dev_view')

    # find minimum number of counts.
    minindex = min(len(company_name),len(exp),len(edu),len(loc),len(date),len(etc),len(info))
    # print(minindex)
    for j in range(int(minindex)):
        try:
            df.loc[20*i + j] = [
            company_name[j].text,                                                   # 회사 이름
            info[j].text.strip(),                                                   # 공고명
            exp[j].text,                                                            # 채용 형태(경력, 신입)
            edu[j].text,                                                            # 학력
            loc[j].text,                                                            # 회사 위치
            ','.join(etc[j].text.split(',')[:5]),                                   # 키워드
            date[j].text,                                                           # 마감 기한
            "https://www.jobkorea.co.kr/" + info[j]['href']                         # 공고 링크
            ]
            page_no += 1

        except:
            print("Index Error")
            page_no += 1
            pass
    page_no += 1
    time.sleep(0.1)

file_name = str(datetime.date.today()) + "_" + str(URLindex) + "_잡코리아_채용공고.csv"
df.to_csv(file_name,index=False, encoding="utf-8-sig")
pd.read_csv(file_name)