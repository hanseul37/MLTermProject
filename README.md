# MLTermProject
Individuals preparing for employment often find it challenging to determine whether their qualifications and portfolios are suitable for a particular company. 
Additionally, with numerous job postings available, some may struggle to identify opportunities that align with their skills. 
To address this, we aimed to create a system that collects information from company job postings, such as majors and fields, and integrates data from reviews by individuals who have worked at these companies. 
By utilizing user portfolios, career history, preferences, and other factors, the system recommends job postings that are suitable for the user. 
Our goal is to develop a practical system, and to achieve this, we trained the model using actual employment data from Korea.

## Skills
<div> 
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Goole Colab-F9AB00?style=for-the-badge&logo=Google Colab&logoColor=white">
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white">
<br>
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white">
<img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">
</div>

## Dataset
### Job announcement details data from Job Planet
JobPlanet's recruitment details crawler.
Crawling the company name, job, major work, qualification requirements, and preferential treatment.
The dynamically assigned link is converted to an absolute path, stored, and then crawled through the link. This method can start crawling again from the desired link even if there is an error in the middle or the connection is disconnected.
It was written as of December 2023, and if the structure of the webpage changes, the code may not work.

### Job announcement data from Job Korea
JobKorea's recruitment data crawler.
Crawling data such as company names, job titles, fields, dates, links, etc., from JobKorea. 
Dynamically collecting data by automatically navigating through pages in the entire regional dataset.

### Company review data from Job Planet
JobPlanet's company review data crawler.
Crawling data on company reviews and ratings from JobPlanet. Since the company codes are not explicitly specified, manually cross-referencing with 200,000 codes for data collection. 
Collecting 5 reviews on each page and automatically navigating through pages for the process.

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

