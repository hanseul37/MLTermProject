from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from endpoint_util import EndpointUtil1, EndpointUtil2
import boto3
import json

# Define local folder path, endpoint names, and S3 bucket name
local_folder_path = '/data/'
endpoint_name1= "blazingtext-2023-12-08-13-54-55-947"
endpoint_name2= "factorization-machines-2023-12-09-06-01-30-551"
bucket_name = "sagemaker-ml1-job"

# Create EndpointUtil instances for each endpoint
endpoint1 = EndpointUtil1(bucket_name, endpoint_name1, local_folder_path)
endpoint2 = EndpointUtil2(bucket_name, endpoint_name2, local_folder_path)

# Define Pydantic models
class KeywordList(BaseModel):
    keywords: List[str]
    
class ReviewList(BaseModel):
    company_name: List[str]
    point: List[int]

# Create a FastAPI app instance
app = FastAPI()

# Endpoint for keyword recommendation
@app.post("/keyword")
async def keyword_recommend(keyword_list: KeywordList):
    keywords = keyword_list.keywords
    pred_result = endpoint1.call(keywords)
    words = [word for word, _ in pred_result]

    return words
    
# Endpoint for review-based recommendation    
@app.post("/review")
async def review_recommend(review_list: ReviewList):
    companies = review_list.company_name
    ratings = review_list.point
    pred_result = endpoint2.call(companies, ratings)
    recommend_company = pred_result["회사명"].tolist()
    return recommend_company

# Run the FastAPI app using uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("server:app", host='0.0.0.0', port=8000, workers=1)
