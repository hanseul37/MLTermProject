# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import chardet

# 파일의 인코딩을 감지
with open('job_details.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large

print(result['encoding'])

data = pd.read_csv("job_details.csv", encoding=result['encoding'])

data = data.replace('#NAME?', np.nan)
data = data.dropna()

# ? 문자를 삭제하는 함수 정의
def remove_question_mark(cell):
    return str(cell).replace('?', '')

# 모든 셀에 대해 함수 적용
data = data.applymap(remove_question_mark)

print(data)