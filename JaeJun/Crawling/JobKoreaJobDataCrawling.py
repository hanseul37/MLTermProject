import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs   
import time
import datetime
from tqdm import trange

# 스크래핑할 웹 사이트의 url을 선언, f-string을 이용해 page number를 바꾸어가며 탐색할 수 있도록 함.
page_no = 1
# url = f"https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D&tabType=recruit&Page_No={page_no}" # 키워드 "데이터 분석" 으로 검색한 쿼리문.
url = f"https://www.jobkorea.co.kr/Search/?local=I000%2CB000%2CK000%2CG000%2C1000%2CO000%2CP000%2CE000%2CL000%2CM000%2CF000%2CD000%2CH000%2CJ000%2CC000%2CA000%2CN000%2CQ000&tabType=recruit&Page_No={page_no}" # 지역 "전체" 으로 검색한 쿼리문.


# url_0 = f"https://www.jobkorea.co.kr/Search/?local=I000&tabType=recruit&Page_No={page_no}"   # 지역 "서울" 으로 검색한 쿼리문.
# url_1 = f"https://www.jobkorea.co.kr/Search/?local=2CB000&tabType=recruit&Page_No={page_no}" # 지역 "경기" 으로 검색한 쿼리문.
# url_3 = f"https://www.jobkorea.co.kr/Search/?local=2CK000&tabType=recruit&Page_No={page_no}" # 지역 "인천" 으로 검색한 쿼리문.
# url_4 = f"https://www.jobkorea.co.kr/Search/?local=2CG000&tabType=recruit&Page_No={page_no}" # 지역 "대전" 으로 검색한 쿼리문.
# url_5 = f"https://www.jobkorea.co.kr/Search/?local=2C1000&tabType=recruit&Page_No={page_no}" # 지역 "세종" 으로 검색한 쿼리문.
# url_6 = f"https://www.jobkorea.co.kr/Search/?local=2CO000&tabType=recruit&Page_No={page_no}" # 지역 "충남" 으로 검색한 쿼리문.
# url_7 = f"https://www.jobkorea.co.kr/Search/?local=2CP000&tabType=recruit&Page_No={page_no}" # 지역 "충북" 으로 검색한 쿼리문.
# url_8 = f"https://www.jobkorea.co.kr/Search/?local=2CE000&tabType=recruit&Page_No={page_no}" # 지역 "광주" 으로 검색한 쿼리문.
# url_9 = f"https://www.jobkorea.co.kr/Search/?local=2CL000&tabType=recruit&Page_No={page_no}" # 지역 "전남" 으로 검색한 쿼리문.
# url_10 = f"https://www.jobkorea.co.kr/Search/?local=2CM000&tabType=recruit&Page_No={page_no}" # 지역 "전북" 으로 검색한 쿼리문.
# url_11 = f"https://www.jobkorea.co.kr/Search/?local=2CF000&tabType=recruit&Page_No={page_no}" # 지역 "대구" 으로 검색한 쿼리문.
# url_12 = f"https://www.jobkorea.co.kr/Search/?local=2CD000&tabType=recruit&Page_No={page_no}" # 지역 "경북" 으로 검색한 쿼리문.
# url_13 = f"https://www.jobkorea.co.kr/Search/?local=2CH000&tabType=recruit&Page_No={page_no}" # 지역 "부산" 으로 검색한 쿼리문.
# url_14 = f"https://www.jobkorea.co.kr/Search/?local=2CJ000&tabType=recruit&Page_No={page_no}" # 지역 "울산" 으로 검색한 쿼리문.
# url_15 = f"https://www.jobkorea.co.kr/Search/?local=2CC000&tabType=recruit&Page_No={page_no}" # 지역 "경남" 으로 검색한 쿼리문.
# url_16 = f"https://www.jobkorea.co.kr/Search/?local=2CA000&tabType=recruit&Page_No={page_no}" # 지역 "강원" 으로 검색한 쿼리문.
# url_17 = f"https://www.jobkorea.co.kr/Search/?local=2CN000&tabType=recruit&Page_No={page_no}" # 지역 "제주" 으로 검색한 쿼리문.
# url_18 = f"https://www.jobkorea.co.kr/Search/?local=2CQ000&tabType=recruit&Page_No={page_no}" # 지역 "전국" 으로 검색한 쿼리문.
# urls = [url_0 ,url_1 ,url_3 ,url_4 ,url_5 ,url_6 ,url_7 ,url_8 ,url_9 ,url_10,url_11,url_12,url_13,url_14,url_15,url_16,url_17,url_18]
# urls.reverse()
# DataFrame 선언
df = pd.DataFrame( columns = ['회사명','공고명','채용 형태(경력, 신입)','학력','직장 위치','키워드','마감 기한','공고 링크'])

# 스크래핑할 웹 사이트의 총 페이지 수 파악
# '총 OOOO건' 이라는 검색 결과를 스크래핑하여 한 페이지당 표시 수인 20으로 나누기

URLindex = 0
# for url in urls: # 한번에 전체 지역을 돌릴 때 터질 위험을 위해 지역별로 분할
URLindex = URLindex + 1
response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
response.encoding = 'cp949'
soup = bs(response.text,'html.parser')

pages = soup.find('p','filter-text').find('strong').text.replace(',','')
pages = round(int(pages)/20)

# For문을 이용해 웹 사이트 탐색
# 바깥의 for문을 통해 페이지를 바꾸어가며 탐색하고
# 안쪽의 for문으로 페이지 내 20개의 공고를 옮겨가며 탐색한다.

for i in trange(pages):                       # for i in trange(pages): 를 통해 전체 페이지 탐색 가능. 시간이 오래걸려 일단 20페이지만 탐색

    # url = f"https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D&tabType=recruit&Page_No={page_no}"

    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    soup = bs(response.text,'html.parser')
    
    company_name = soup.find_all('a','name dev_view')
    exp = soup.find_all('span','exp')
    edu = soup.find_all('span','edu')
    loc = soup.find_all('span','loc long')
    date = soup.find_all('span','date')
    etc = soup.find_all('p','etc')
    info = soup.find_all('a','title dev_view')

    for j in range(len(etc)):
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

        except NameError as e:
            print("Index Error", e.args)
            page_no += 1
    page_no += 1
    time.sleep(0.1)

file_name = str(datetime.date.today()) + "_" + str(URLindex) + "_잡코리아_채용공고.csv"
df.to_csv(file_name,index=False, encoding="utf-8-sig")
pd.read_csv(file_name)