import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs   
import time
import datetime
from tqdm import trange

# 스크래핑할 웹 사이트의 url을 선언, f-string을 이용해 page number를 바꾸어가며 탐색할 수 있도록 함.
page_no = 1
url = f"https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D&tabType=recruit&Page_No={page_no}"

# DataFrame 선언
df = pd.DataFrame( columns = ['회사명','공고명','채용 형태(경력, 신입)','학력','직장 위치','키워드','마감 기한','공고 링크'])

# 스크래핑할 웹 사이트의 총 페이지 수 파악
# '총 OOOO건' 이라는 검색 결과를 스크래핑하여 한 페이지당 표시 수인 20으로 나누기

response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
soup = bs(response.text,'html.parser')

pages = soup.find('p','filter-text').find('strong').text.replace(',','')
pages = round(int(pages)/20)

# For문을 이용해 웹 사이트 탐색
# 바깥의 for문을 통해 페이지를 바꾸어가며 탐색하고
# 안쪽의 for문으로 페이지 내 20개의 공고를 옮겨가며 탐색한다.

for i in trange(20):                       # for i in trange(pages): 를 통해 전체 페이지 탐색 가능. 시간이 오래걸려 일단 20페이지만 탐색

    url = f"https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D&tabType=recruit&Page_No={page_no}"

    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    soup = bs(response.text,'html.parser')
    
    company_name = soup.find_all('a','name dev_view')
    exp = soup.find_all('span','exp')
    edu = soup.find_all('span','edu')
    loc = soup.find_all('span','loc long')
    date = soup.find_all('span','date')
    etc = soup.find_all('p','etc')
    info = soup.find_all('a','title dev_view')



    for j in range(20):
        # print(','.join(etc[j].text.split(',')[:5]),)
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
        except:
            print()
    page_no += 1
    
    time.sleep(0.1)

file_name = str(datetime.date.today()) + "_데이터분석_채용공고.csv"
df.to_csv(file_name,index=False)
pd.read_csv(file_name)