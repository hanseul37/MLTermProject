import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib3
from tqdm import trange

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# soup = bs(response.text,'html.parser')

# pages = soup.find('p','filter-text').find('strong').text.replace(',','')


# last_page = 212
last_page = 100 # 임시로 1
# lastCompanyIndex = 25833     # companyIndex : 1 ~ 25833
lastCompanyIndex = 40000     # 임시로

for companyIndex in trange(1, lastCompanyIndex):

    # url = 'https://www.jobplanet.co.kr/companies/' + str(companyIndex) + '? page='+str(1)
    # res = session.get(url) 
    # res.raise_for_status()

    # soup = BeautifulSoup(res.text, 'html.parser')

    # title = soup.find('h2', class_ = 'stats_ttl')
    # # pages = title.find('h2')
    # # print(pages.get_text().strip())
    # # title = title.get_text()
    # print(title)

    # exit()

    # samsung = str(30139)
    # print("")
    # print("get soup from request....")

    for idx in trange(1, last_page):
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
            # print("No Company on id " + str(companyIndex) )
            pass

    # try:
    for k in trange(5):  # 한페이지에 리뷰 5개씩 나오기 때문에 k=5
        print("")
        print("Flag")
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
        # print("content : " + str(content))
        # exit()

        # 장단점 경영진 의견                                                                    
        merit = soup.select('dl.tc_list > dd.df1 > span')[0 + count3].text                      # 장점
        disadvantages = soup.select('dl.tc_list > dd.df1>span') [1 + count3].text               # 단점
        df_tit = soup.select('dl.tc_list > dd.df1> span') [2 + count3].text                     # 바라는점                                                                               
        
        reviewer_info = [companyIndex , position, status, loc, day, star_rating, promotion, welfare, balance, culture,
        top, clean_str(content), clean_str(merit), clean_str(disadvantages), clean_str(df_tit)]
        # top, content, merit, disadvantages, df_tit]

        result.append(reviewer_info)
        reviewer_info=[]
        count3 += 3
        count4 += 4
        count5 += 5
        print("pass :"+str(idx)+"-"+str(k))
        print("result : " + str(result))
    # except :

    # print("@@@")
    # print("fail" + str(idx))
    # pass

    colname = ['회사명', '직무','상황', '지역', '작성일', '총점', '승진 기회 및 가능성', '복지 및 급여', '업무와 삶의 균형', '사내문화', '경영진', '총평', '장점', '단점', '바라는점']
    df = pd.DataFrame(result, columns=colname)
    print("")

#저장을 희망하는 파일명으로 저장
file_name = "jobPlanet_companyReview.csv"
df.to_csv(file_name,index=False, encoding="utf-8-sig")





print(result)