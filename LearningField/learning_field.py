from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
import pandas as pd

data = pd.read_csv("new_programmers.csv")

# 각 직무별로 기술 스택을 한 문장으로 합침
job_to_stacks = {}
for i in range(len(data)):
    jobs = data['section-summary'][i].split(',')
    stacks = set(eval(data['section-stack'][i])) # set을 사용하여 중복된 기술 스택 제거
    for job in jobs:
        if job in job_to_stacks:
            job_to_stacks[job] = job_to_stacks[job].union(stacks) # set의 union 메서드를 사용하여 기술 스택 합침
        else:
            job_to_stacks[job] = stacks

# 각 직무별 기술 스택을 다시 한 문장으로 합침
for job, stacks in job_to_stacks.items():
    job_to_stacks[job] = ' '.join(stacks)

cvec = CountVectorizer(ngram_range=(1,2))

# CountVectorizer를 사용하여 각 직무의 기술 스택을 벡터화함
X = cvec.fit_transform(job_to_stacks.values())

# TfidfVectorizer를 사용하여 TF-IDF 점수를 계산함
tfidf_vectorizer = TfidfVectorizer(use_idf=True)
X_tfidf = tfidf_vectorizer.fit_transform(job_to_stacks.values())

# 각 직무별로 TF-IDF 점수가 가장 높은 기술 스택을 추출함
indices = np.argsort(tfidf_vectorizer.idf_)[::-1]
features = tfidf_vectorizer.get_feature_names_out()

# 직무와 해당 직무의 기술 스택을 함께 출력
for job, tfidf_vector in zip(job_to_stacks.keys(), X_tfidf.toarray()):
    top_indices = np.argsort(tfidf_vector)[::-1]
    top_features = [features[i] for i in top_indices[:10]]
    print(f"{job}: {top_features}")