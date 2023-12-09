import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# server
import time


@st.cache_data()
def request_endpoint(url, user_keywords):
    payload = {"keywords": user_keywords}
    response = requests.post(url, json=payload)
    st.write(response.status_code)
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        return result
    return None

def request_companyRecommend(url, company_name, point):
    payload = {"company_name": company_name, "point": point}
    response = requests.post(url, json=payload)
    st.write(response.status_code)
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        return result
    return None

page1_name = "추천"
page2_name = "장르 분포"
st.sidebar.subheader("SageMaker Endpoint")
page = st.sidebar.selectbox("페이지 선택", [page1_name, page2_name])
api_url = st.sidebar.text_input('fast api', value="3.26.64.95:8000")

st.title("Content based recommendation")

#추가한 UI
keywords = st.text_input("키워드를 입력하세요", "모바일, 데이터")


keyword = keywords.replace(" ","")
keyword = keyword.split(',')

st.write("입력한 keyword : ", keyword) # 

#request predict 
try:
    url = f"http://{api_url}/keyword"
    pred_result = request_endpoint(url,keyword)
    st.write("pred_result : ", pred_result) # 

except:
    time.sleep(1)
    st.write("retry...")
    url = f"http://{api_url}/keyword"
    pred_result = request_endpoint(url,keyword)

    
st.title("collaborate based recommendation")

company_names = st.text_input("회사를 입력하세요", "협성기전, 지에스건설")
company_name = company_names.replace(" ","")
company_name = company_name.split(',')
st.write("회사 : ", company_name) # 

#option = st.selectbox("평점을 선택하세요", ["1","2","3","4","5","6","8","9","9","10"])
#st.write(f"선택된 옵션: {option}")


## model 2 - collaborate based recommendation
def request_companyRecommend(url, company_name, point):
    payload = {"company_name": company_name, "point": point}
    response = requests.post(url, json=payload)
    st.write(response.status_code)
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        return result
    return None

api_url2 = "3.26.64.95:8000"

points = st.text_input("평점을 입력하세요(1-10)", "1,2")
point = points.replace(" ","")
point = point.split(',')
st.write("회사사 : ", point) # 

if len(company_name) != len(point):
    st.write("Error : 회사와 평점의 수가 맞지 않습니다")
    
else:
    try:
        #st.write("RUN")
        url = f"http://{api_url2}/review" #/keyword --> change
        pred_result = request_companyRecommend(url,company_name,point) # keyword
        st.write("추천하는 기업 : ", pred_result)
        
    except:
        time.sleep(1)
        st.write("retry...")
        url = f"http://{api_url2}/review" #/keyword --> change
        pred_result = request_companyRecommend(url,company_name,point) # keyword
        st.write("추천하는 기업 : ", pred_result)















#
#t.title("Movie Recommendations")
#f st.sidebar.button('Get Recommendations'):
#   # FastAPI 엔드포인트 api
#   url = f"http://{api_url}/{user_id}/{threshold}"
#   pred_df = request_endpoint(url)
#   
#   # FastAPI 영화 정보 api
#   url = f"http://{api_url}/get_movie_info"
#   movies_df = request_endpoint(url)

#   # movie 정보와 merge
#   all_df = pd.merge(pred_df, movies_df, on='movieId', how='inner')        
#       
#   if page == page1_name:
#       # bar chart 표시
#       st.bar_chart(all_df.set_index('title')['prediction'])
#       
#       # DataFrame 표시
#       st.dataframe(all_df)
#       
#       # 예측값 시각화
#       st.line_chart(all_df['prediction'])
#       st.line_chart(all_df.set_index('title')['prediction'])
#   
#   elif page == page2_name:
#       # Streamlit 앱 시작
#       st.title('장르 분포')
#       
#       # DataFrame 표시
#       st.dataframe(all_df)
#       print(all_df)
#       
#       # 가로 막대 차트
#       st.subheader("예측값 막대 차트")
#       st.bar_chart(all_df['prediction'], use_container_width=True)
#       
#       # 산점도
#       st.subheader("예측값 산점도")
#       plt.figure(figsize=(8, 6))
#       plt.scatter(all_df['title'], all_df['prediction'])
#       plt.xlabel('movieTitle')
#       plt.ylabel('prediction')
#       st.pyplot(plt)
#       
#       # 장르 데이터 전처리: '|'로 구분된 장르를 분리
#       genre_counts = all_df['genres'].str.split('|').explode().value_counts()
#       st.write(genre_counts)
#       
#       # 파이 차트 그리기
#       fig, ax = plt.subplots()
#       ax.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=90)
#       ax.axis('equal')  # 원형 파이 차트로 조정
#       
#       # 파이 차트를 Streamlit에 표시
#       st.pyplot(fig)