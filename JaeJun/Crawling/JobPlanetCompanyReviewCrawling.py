import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib3
from tqdm import trange
import time
import datetime
import argparse
import os, sys, pickle

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('-first',  type=int, default=1)
parser.add_argument('-last',  type=int, default=2)
args = parser.parse_args()

login_url = 'https://www.jobplanet.co.kr/users/sign_in'

#email 본인 아이디 password 본인 패스워드 입력. 단 리뷰를 남겨서 전체 접근이 가능한 상태여야 함
email = '3636qq@gachon.ac.kr'
password = 'qkrwowns123!@'

LOGIN_INFO ={
'user[email]' : email,
'user[password]' : password,
'commit' : '로그인'
}

session = requests.session()
response = session.post(login_url, data = LOGIN_INFO, verify = False)

if response.status_code == 200:
    print("로그인 성공")
else:
    print("로그인 실패")
    print("status_code : " + str(response.status_code))



response.raise_for_status()

result = []
def clean_str(text):
    # pattern = '([ㄱ-ㅎㅏ-ㅣ]+)' # 한글 자음, 모음 제거
    # text = re.sub(pattern=pattern, repl='', string=text) 
    pattern = '[^>]*'   #HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s]*'   #특수 기호 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    text.replace('\r', '.')
    return text

#uTl 은 보고싶은 기업의 리뷰 URL 이며 마지막은 ?page= 형태로 해야함, last_page는 해당 기업 리뷰의 마지막 페이지 입력 


# last_page = 212
# last_page = 10 # 임시로 1
# lastCompanyIndex = 25833     # companyIndex : 1 ~ 25833
lastCompanyIndex = 10000     # 임시로
reviewCountKeyword1 = '기업정보'
reviewCountKeyword2 = '기업리뷰'
reviewCountKeyword3 = '리뷰평점'
reviewCount = 0



def CrawlCompanyReviewData(startCompanyCode, lastCompanyCode):
    for companyIndex in range(startCompanyCode, lastCompanyCode):

    # 전체 리뷰/5로 최대 페이지 수 구함
        # url = 'https://www.jobplanet.co.kr/companies/' + str(companyIndex) + '? page='+str(1)

        # try:    # 기업 코드가 있는 경우
        print("")
        print("Company CODE : " + str(companyIndex))
        url = 'https://www.jobplanet.co.kr/companies/' + str(companyIndex) + '? page='+str(1)
        res = session.get(url) 
        res.raise_for_status()
        if res.status_code != 200:
            continue

        else:
            #print("res : " + str(res))
            soup = BeautifulSoup(res.text, 'html.parser')
            soup = soup.prettify() # 보기좋게 구분
            fulltext = soup.split('\n')
            status = ""
            # print(fulltext)
            for i in fulltext:
                if reviewCountKeyword1 in i and reviewCountKeyword2 in i and reviewCountKeyword3 in i:
                    print(i)
                    status = i
                    break

            status = status.split()
            #print(len(status))
            if len(status) == 0:
                print("CASE : No Company")
                continue
            status[5] = status[5].strip('건,')

            companyName = str(status[0])
            if int(status[5]) <= 5:
                print("CASE : No Review")
                continue

            else :
                print(int(status[5]))
                #print("CASE : Riview exist")
                reviewCount = int(status[5])
                maxPageCount = int(reviewCount/5 + 1)
                #print("maxPageCount : " + str(maxPageCount))


            for idx in trange(1, maxPageCount):
                try:
                    # url = 'https://www.jobplanet.co.kr/companies/' + str(companyIndex) + '? page='+str(idx)
                    url = 'https://www.jobplanet.co.kr/companies/' + str(companyIndex) + '? page='+str(idx)
                    res = session.get(url) 
                    res.raise_for_status()

                    soup = BeautifulSoup(res.text, 'html.parser')
                    count3 = 0
                    count4 = 0
                    count5 = 0
                except:
                    #print("No Company on id " + str(companyIndex) )
                    print("CASE : out")
                    continue

            # try:
                for k in range(5):  # 한페이지에 리뷰 5개씩 나오기 때문에 k=5
                    reviewer_info = []

                    # 응답자 정보
                    position = soup.select('.content_top_ty2 > span.txt1') [0 + count4].text                # 직무
                    status   = soup.select('.content_top_ty2 > span.txt1') [1 + count4].text                # 상황
                    loc      = soup.select('.content_top_ty2 > span.txt1') [2 + count4].text                # 지역
                    day      = soup.select('.content_top_ty2 > span.txt1') [3 + count4].text                # 작성일

                    #점
                    star_rating = soup.select('.us_star_m > div.star_score') [0+k] ['style'] [6:-1]         # 총점

                    # rating 5*5
                    promotion = soup.select('.bl_score') [0 + count5] ['style'][6:-1]                       # 승진 기회 및 가능성
                    welfare   = soup.select('.bl_score') [1 + count5] ['style'][6:-1]                       # 복지 및 급여
                    balance   = soup.select('.bl_score') [2 + count5] ['style'][6:-1]                       # 업무와 삶의 균형
                    culture   = soup.select('.bl_score') [3 + count5] ['style'][6:-1]                       # 사내 문화
                    top       = soup.select('.bl_score') [4 + count5] ['style'][6:-1]                       # 경영진

                    # 중심 제목
                    content = soup.select('h2.us_label')[0 + k].text                                        # 총평

                    # 장단점 경영진 의견                                                                    
                    merit = soup.select('dl.tc_list > dd.df1 > span')[0 + count3].text                      # 장점
                    disadvantages = soup.select('dl.tc_list > dd.df1>span') [1 + count3].text               # 단점
                    df_tit = soup.select('dl.tc_list > dd.df1> span') [2 + count3].text                     # 바라는점                                                                               
                    
                    reviewer_info = [companyName , position, status, loc, day, star_rating, promotion, welfare, balance, culture,
                    top, content, merit, disadvantages, df_tit]
                    # top, clean_str(content), clean_str(merit), clean_str(disadvantages), clean_str(df_tit)]

                    result.append(reviewer_info)
                    reviewer_info=[]
                    count3 += 3
                    count4 += 4
                    count5 += 5
            # except :


    colname = ['회사명', '직무','상황', '지역', '작성일', '총점', '승진 기회 및 가능성', '복지 및 급여', '업무와 삶의 균형', '사내문화', '경영진', '총평', '장점', '단점', '바라는점']
    df = pd.DataFrame(result, columns=colname)

    #저장을 희망하는 파일명으로 저장
    file_name = str(datetime.date.today())+"_" + str(startCompanyCode) + "_" +"jobPlanet_companyReview2.csv"
    df.to_csv(file_name,index=False, encoding="utf-8-sig")




if __name__ == "__main__":
    argv = sys.argv
    CrawlCompanyReviewData(args.first, args.last)