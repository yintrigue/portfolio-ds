Tim Chen  
Data Scientist & Product Manager  
Update: 05.05.2021  

Jump To:  
[Machine Learning](#machine_learning)  
[Statistical Analysis](#statistical_analysis)  
[Data Exploration](#data_exploration)  
[Bonus: UX & Photography](#others)    

<a name="machine_learning"></a>

## Machine Learning

### [NT5?! Training T5 to Perform Numerical Reasoning](./ml_nt5)  

**Final Model**: T5, SentencePiece  
**Baseline Model**: BERT  
**Tech Stack**: TensorFlow, HuggingFace, Scikit-learn, TPU, GCS      

*NT5?! Training T5 to Perform Numerical Reasoning* is a NLP research on **NRoT** (numerical reasoning over text) using **T5**. A total of **6 datasets** including DROP, SQuAD, and 4+GB of synthetically generated data are used for training/testing T5-Small and T5-Base. We are currently in the process of refining the research in response to feedback from the ACL submission.    

### [Predicting Flight Delays](./ml_flight_delays)  

**Final Model**: Gradient Boosted Tree, Distributed Computing  
**Baseline Models**: XGBoost Tree, Random Forest, Logistic Regression, SVM   
**Tech Stack**: PySpark, Scikit-learn, Databricks, AWS   

Flight delays are costly — the delay cost per minute was estimated to be $74.24 for the airline in 2019. The study attempts to tackle the problem by building a **distributed machine learning pipeline** using PySpark to predict flight delays. A total of **5 datasets**, including 1GB+ of flight records and 25GB+ of global weather information from 2015 to 2019, are used. The datasets are **imbalanced**, with only 20% of the data being positive. The final model is trained on an AWS cluster with **five r4.xlarge nodes** through Databricks.

### [Classifying Melanoma](./ml_melanoma)  

**Final Model**: EfficientNet-B07  
**Baseline Models**: CNN, CNN + Feedforward NN (Concatenation), Logistic Regression, SVM, PCA, Focal Loss  
**Tech Stack**: TensorFlow, Keras, Scikit-learn, TPU, GCS    

*SIIM-ISIC Melanoma Classification* is an annual Kaggle competition on identifying the deadly skin cancer, Melanoma, based on patient metadata and images of skin lesions. The **two datasets** (textual patient metadata + 40GB image pool) include 33,126 records, of which **only 584 examples are positive (1.76%)**. Three neural networks and two baseline models, Logistic Regression and SVM, are built for the classification.

### [Visualizing EfficientNet](./ml_visualizing_neural_net)  
**Models:** EfficientNet-B0, PCA, Focal Loss  
**Tech Stack:** TensorFlow, Keras, TPU, GCS     

The study explores ways to visualize the learning progress of **EfficientNet** (a convolutional neural network published by Google in 2019) by extracting embeddings and projecting the extracted features onto a 2D plane using **PCA**.

### [Neural Snaky](./ml_snaky) 
**Final Model**: Neural Network  
**Baseline Model**: Logistics  
**Tech Stack:** TensorFlow, Scikit-learn, PyGame     

*Snaky* is a PyGame implementation of the classic game, Snake. There is a twist: **the snake plays the game by itself** with a brain made of a neural network!  

<a name="statistical_analysis"></a>

## Statistical Analysis

### [Field Experiment: Gender Bias in Auto Repair Pricing](./st_gender_bias)  

**Keywords**: Randomized Field Experiment, 2x2 Factorial Design, Blocking, Power Analysis, OLS, ANOVA  
**Tech Stack**: R  

*Gender Bias in Auto Repair Pricing* is a statistical research with a **randomized field experiment** from end to end including the experiment design, pilot/power study, data collection/engineering, and model building/analysis. 

### [Regression: Quality on Popularity for YouTube Videos](./st_youtube)  

**Keywords**: OLS, Gauss-Markov Assumptions, Omitted Variable Bias  
**Tech Stack**: R

The study includes a **regression analysis**, including an examination of **Gauss–Markov assumptions** and **omitted variable bias**, in an attempt to explore the relationship between YouTube video's quality and viewership. In particular, we ask the question: How does the quality of a video affect its number of views?   

<a name="data_exploration"></a>

## Data Exploration  

### [AwesomeBabyNames](./py_awesome_baby_names)  
**Tech Stack**: MVC, SQLite, Python  

An awesome baby starts with an awesome name! *AwesomeBabyNames* is a Python app that helps you come up with a great name for your baby by visualizing **100+ years of census data** collected by the US government.

### [Visualizing Death-Zone Mountaineering](./py_himalayan_db)  
**Tech Stack:** Plotly, Seaborn, GeoPy, Pandas, NumPy, Python  

*Death-Zone Mountaineering* is an analysis on expeditions to the 16 eight-thousander peaks (i.e. peaks with altitudes above 8,000m) in the Himalayas mountain range. The data visualization project is primarily based on the *Himalayan Database*, covering **over 100 years of expeditions** from 1905 through Spring 2019.  

### [SQL: Promoting Lyft Bay Wheels](./py_lyft_bay_wheels)  

**Tech Stack:** SQL, BigQuery, Plotly, Python   

The goal of the study is to help Bay Wheels **increase its ridership** by developing **promotional strategies** based on data analytics. The two datasets used for the analysis, Bikeshare Trips and Stations, are hosted on GCP through BigQuery. **SQL queries** are used extensively to extract insights from raw data.  

<a name="others"></a>

## Bonus: UX & Photography

### [UX: Yintegral.com](https://yintegral.com/)  

**Keywords**: UX Portfolio  
**Tech Stack:** Java, PHP, JavaScript, jQuery, HTML/CSS  

[Yintegral.com](https://yintegral.com/) is a portfolio of my **select UX projects**. Before data science I was a dev lead in a WPP UX design agency, leading e-commerce and web development for clients including Nike and EA Game (e.g. online stores, web analytics, data visualization, in-store kiosks, etc.). I also worked as a contract UX designer at my own free time.  

### [Photography: Yintrigue.com](https://yintrigue.com/)  
**Keyword**: Photography Portfolio  
**Tech Stack:** Nikon  

I am a photographer at my own free time and love traveling around the world to explore nature. <a href="https://yintrigue.com" target="_blank">Yintrigue.com</a> is the photography portfolio that I built to showcase my **15+ years of works** around the world. 

### [Photography: Hello, Baby Clara!](./sp_hello_baby_clara)  

**Keywords**: Single-page Web App, Photography  
**Tech Stack:** JavaScript, jQuery, PHP, HTML/CSS  

*Hello, Baby Clara!* is a photo diary that I built to document my daughter's growing up. It is a database-free **SPA (single-page application)** designed for storytelling, and allows me to publish photos with metadata automatically parsed with a fully customizable layout. The experience is to be enjoyed by both the farther (me) and daughter (Clara)! 😃