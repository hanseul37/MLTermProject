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

#email , password . 
# It should be accesible for all reviews
email = '******@gachon.ac.kr' # hide for personal information
password = '*************'    # hide for personal information

LOGIN_INFO ={
'user[email]' : email,
'user[password]' : password,
'commit' : '로그인'
}

# send request for login

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
    pattern = '[^>]*'   # Delete HTML Tag
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s]*'   # Delete symbols
    text = re.sub(pattern=pattern, repl='', string=text)
    text.replace('\r', '.')
    return text

# It should be done with "?page=", last_page means number of last page index


reviewCountKeyword1 = '기업정보'
reviewCountKeyword2 = '기업리뷰'
reviewCountKeyword3 = '리뷰평점'
reviewCount = 0


# define function for CMD, with input startCompanyIndex and lastCompanyCode
# Every company have their own company code, but it is not regular. Whole company number is 25430 but something's code is 130,000
# So try all company_code until 200,000. If there is no Company on company code, it passed

def CrawlCompanyReviewData(startCompanyCode, lastCompanyCode):
    for companyIndex in range(startCompanyCode, lastCompanyCode):

        print("")
        print("Company CODE : " + str(companyIndex))
        url = 'https://www.jobplanet.co.kr/companies/' + str(companyIndex) + '? page='+str(1)
        res = session.get(url) 
        res.raise_for_status()
        
        # check failure
        if res.status_code != 200:
            continue

        else:
            soup = BeautifulSoup(res.text, 'html.parser')
            soup = soup.prettify() # divide for visibility
            fulltext = soup.split('\n')
            status = ""

            # should find out whole page numbers so find string include keyword "기업 평점"
            for i in fulltext:
                if reviewCountKeyword1 in i and reviewCountKeyword2 in i and reviewCountKeyword3 in i:
                    print(i)
                    status = i
                    break

            status = status.split()
            # check if company exist on the company code
            if len(status) == 0:
                print("CASE : No Company")
                continue

            # define count of whole review number with keyword "건"
            count = ""
            for i in range(5,len(status)):
                if '건' in status[i]:
                    count = status[i]
            
            # extract count
            status[5] = count.replace('건,','')
            status[5] = status[5].replace(',','')
            
            companyName = str(status[0])
            if int(status[5])%5 == 0:
                print("CASE : No Review")
                continue
                
            else :
                print(int(status[5]))
                reviewCount = int(status[5])
                maxPageCount = int(reviewCount/5)


            for idx in trange(1, maxPageCount):
                # get sources in each page
                try:
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

                # extract dataset from each review
                try:
                    for k in range(5):  # There are 5 reviews in each page
                        reviewer_info = []

                        # information about reviewer
                        position = soup.select('.content_top_ty2 > span.txt1') [0 + count4].text                # 직무
                        status   = soup.select('.content_top_ty2 > span.txt1') [1 + count4].text                # 상황
                        loc      = soup.select('.content_top_ty2 > span.txt1') [2 + count4].text                # 지역
                        day      = soup.select('.content_top_ty2 > span.txt1') [3 + count4].text                # 작성일

                        # score
                        star_rating = soup.select('.us_star_m > div.star_score') [0+k] ['style'] [6:-1]         # 총점

                        # rating 5*5
                        promotion = soup.select('.bl_score') [0 + count5] ['style'][6:-1]                       # 승진 기회 및 가능성
                        welfare   = soup.select('.bl_score') [1 + count5] ['style'][6:-1]                       # 복지 및 급여
                        balance   = soup.select('.bl_score') [2 + count5] ['style'][6:-1]                       # 업무와 삶의 균형
                        culture   = soup.select('.bl_score') [3 + count5] ['style'][6:-1]                       # 사내 문화
                        top       = soup.select('.bl_score') [4 + count5] ['style'][6:-1]                       # 경영진

                        # 
                        content = soup.select('h2.us_label')[0 + k].text                                        # 총평

                        # dis/advantages                                                                    
                        merit = soup.select('dl.tc_list > dd.df1 > span')[0 + count3].text                      # 장점
                        disadvantages = soup.select('dl.tc_list > dd.df1>span') [1 + count3].text               # 단점
                        df_tit = soup.select('dl.tc_list > dd.df1> span') [2 + count3].text                     # 바라는점                                                                               
                        
                        # put in list
                        reviewer_info = [companyName , position, status, loc, day, star_rating, promotion, welfare, balance, culture,
                        top, content, merit, disadvantages, df_tit]

                        result.append(reviewer_info)
                        reviewer_info=[]
                        count3 += 3
                        count4 += 4
                        count5 += 5
                except :
                    pass


    colname = ['회사명', '직무','상황', '지역', '작성일', '총점', '승진 기회 및 가능성', '복지 및 급여', '업무와 삶의 균형', '사내문화', '경영진', '총평', '장점', '단점', '바라는점']
    df = pd.DataFrame(result, columns=colname)

    # save file with the file_name
    file_name = str(datetime.date.today())+"_" + str(startCompanyCode) + "_" +"jobPlanet_companyReview2.csv"
    df.to_csv(file_name,index=False, encoding="utf-8-sig")




if __name__ == "__main__":
    argv = sys.argv
    CrawlCompanyReviewData(args.first, args.last)