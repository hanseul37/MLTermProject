import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

login_url = 'https://www.jobplanet.co.kr/users/sign_in'

#email 본인 아이디 password 본인 패스워드 입력. 단 리뷰를 남겨서 전체 접근이 가능한 상태여야 함
email = '3636qq'
password = 'qkrwowns123!@'

LOGIN_INFO ={
'user [email]' : email,
'user [password]' : password,
'commit' : '로그인'
}

session = requests.session()
res = session.post(login_url, data = LOGIN_INFO, verify = False)
res.raise_for_status()
result = []
def clean_str(text):
    pattern = '([ᄀ-하-[]+)' # 한글 자음, 모음 제거 text = re.sub(pattern-pattern, repl='', string text) pattern <[^>]*>' # HTML EHI THI JI
    text = re.sub(pattern-pattern, repl='', string=text) 
    pattern = '[^>]*'   #HTML 태그 제거
    text = re.sub(pattern-pattern, repl='', string=text)
    pattern = '[^\w\s]*'   #특수 기호 제거
    text = re.sub(pattern-pattern, repl='', string=text)
    text.replace('\r', '.')
    return text

#uTl 은 보고싶은 기업의 리뷰 URL 이며 마지막은 ?page= 형태로 해야함, last_page는 해당 기업 리뷰의 마지막 페이지 입력 
last_page = 212
for idx in range(1, last_page):
    # 주소는 현대 엔지니어링
    url = 'https://www.jobplanet.co.kr/companies/1322/reviews/%ED%98%84%EB%8C%80%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81? page='+str(idx)
    res = session.get(url) 
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')

    count3 =0
    count4 =0
    count5=0


try:
    for k in range(5):
        reviewer_info = []
        # 응답자 정보
        position = soup.select('.content_top_ty2 > span.txt1')[0+ count4].text 
        status = soup.select('.content_top_ty2 > span.txt1')[1 + count4].text 
        loc = soup.select('.content_top_ty2 > span.txt1') [2 + count4].text

        day = soup.select('.content_top_ty2 > span.txt1') [3+ count4].text
        #점 
        star_rating = soup.select('.us_star_m > div.star_score') [0+k] ['style'] [6:-1]

        # rating 5*5
        promotion = soup.select('.bl_score')[0+ count5]['style'][6: -1] 
        welfare = soup.select('.bl_score') [1 + count5] ['style'][6:-1] 
        balance = soup.select('.bl_score') [2+ count5] ['style'][6: -1] 
        culture = soup.select('.bl_score') [3+ count5] ['style'][6:-1]
        top = soup.select('.bl_score') [4 + count5] ['style'][6:-1] 
        
        # 중심 제목
        content = soup.select('h2.us_label')[0+k].text

        # 장단점 경영진 의견
        merit = soup.select('dl.tc_list > dd.df1 > span')[0+ count3].text 
        disadvantages = soup.select('dl.tc_list > dd.df1>span') [1 + count3].text
        df_tit = soup.select('dl.tc_list > dd.df1> span') [2+ count3].text
        
        reviewer_info = [position, status, loc, day, star_rating, promotion, welfare, balance, culture,
        top,clean_str(content), clean_str(merit), clean_str(disadvantages), clean_str(df_tit)]

        result.append(reviewer_info)
        reviewer_info=[]
        count3 += 3
        count4 += 4
        count5 += 5
        print("pass :"+str(idx)+"-"+str(k))
except :
    print("fail" + str(idx))
    pass
    
colname = ['직무','상황', '지역', '작성일', '총점', '승진 기회 및 가능성', '복지 및 급여', '업무와 삶의 균형', '사내문화', '경영진','총', '평', '장점', '단점', '바라는점']
df = pd.DataFrame(result, columns=colname)
#저장을 희망하는 파일명으로 저장
df.to_excel ("jobplanet_19.xlsx")




print(result)