# MLTermProject
Individuals preparing for employment often find it challenging to determine whether their qualifications and portfolios are suitable for a particular company. 
Additionally, with numerous job postings available, some may struggle to identify opportunities that align with their skills. 
To address this, we aimed to create a system that collects information from company job postings, such as majors and fields, and integrates data from reviews by individuals who have worked at these companies. 
By utilizing user portfolios, career history, preferences, and other factors, the system recommends job postings that are suitable for the user. 
Our goal is to develop a practical system, and to achieve this, we trained the model using actual employment data from Korea.

## Skills
<div> 
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Goole Colab-F9AB00?style=for-the-badge&logo=Google Colab&logoColor=black">
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white">
<br>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white">
<img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">
</div>

## Dataset


## Funtions
### Company Recommendation System (Model Based CF)
Sagemaker's Factoring Machine model was used to create a model-based CF system using sagemaker.
Amazon SageMaker Factorization Machines (FM) is a machine learning algorithm designed for recommendation and regression tasks. It falls under the class of collaborative filtering algorithms, commonly used for making personalized recommendations based on user behavior or preferences.
Based on the ratings of companies left behind while working, we recommend companies that deserve high ratings from users.

### Keyword Recommendation System (Content Based Filtering)
To proceed with content-based filtering in Sagemaker, we created a BlazingText model of Sagemaker.
Amazon SageMaker BlazingText is a natural language processing (NLP) algorithm that allows you to train and deploy text classification models, word2vec models, and document embeddings. It is built on the Word2Vec algorithm and offers efficient training on large datasets with a focus on word embeddings.
Based on the keywords entered by the user, we recommend other keywords that the user can learn with interest.

## Member
201735833 박재준<br>
201835848 서동익<br>
201935113 이한슬<br>
202035331 박가현<br>

