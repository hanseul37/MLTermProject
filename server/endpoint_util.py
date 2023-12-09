import os
import io
import numpy as np
import pandas as pd
from sagemaker.s3 import S3Downloader
from sagemaker.predictor import Predictor
from gensim.models import KeyedVectors
from surprise import SVD, Dataset, Reader

class EndpointUtil1:
    def __init__(self, bucket_name, endpoint_name, local_folder_path):
        self.bucket_name = bucket_name
        self.endpoint_name = endpoint_name
        self.local_folder_path = local_folder_path
        self.predictor = Predictor(endpoint_name)
   
    def call(self, keywords):
        # Load pre-trained word vectors
        word_vectors = KeyedVectors.load_word2vec_format('vectors.txt', binary=False, encoding='utf-8')

        # Perform word similarity calculation
        result = word_vectors.most_similar(keywords, topn=10)
        
        return result
    
class EndpointUtil2:
    def __init__(self, bucket_name, endpoint_name, local_folder_path):
        self.bucket_name = bucket_name
        self.endpoint_name = endpoint_name
        self.local_folder_path = local_folder_path
        self.predictor = Predictor(endpoint_name)
        
    def call(self, companies, ratings):
        data = pd.read_csv("preprocessed_review.csv")
        
        # Create a Reader object for the Surprise library
        reader = Reader(rating_scale=(0, 100))
       
        # Convert data to Surprise dataset
        surprise_data = Dataset.load_from_df(data[['직무, 지역', '회사명', '총점']], reader)

        # Use the entire dataset for training
        trainset = surprise_data.build_full_trainset()

        # Create an SVD model
        model = SVD()

        # Train the model
        model.fit(trainset)
        
        # User ratings
        user_ratings = pd.DataFrame({'회사명': companies, '평점': ratings})

        # List of companies rated by the example user   
        rated_companies = user_ratings['회사명'].tolist()

        # List of companies not rated by the example user
        unrated_companies = [company for company in data['회사명'].unique() if company not in rated_companies]

        # Predict ratings for companies not rated by the example user
        predictions = [(company, model.predict('직무, 지역', company).est) for company in unrated_companies]

        # Convert the prediction results to a DataFrame
        recommendations_df = pd.DataFrame(predictions, columns=['회사명', '평점'])

        # Sort recommendations by predicted ratings in descending order and select the top 10
        top_n_recommendations = recommendations_df.sort_values(by='평점', ascending=False).head(10)
        
        return top_n_recommendations
