# Predicting Flight Delays

**Final Model**: Gradient Boosted Tree
**Baseline Models**: XGBoost Tree, Random Forest, Logistic Regression, SVM   
**Tech Stack**: PySpark, Scikit-learn, Databricks, AWS   

Flight delays are costly — the delay cost per minute was estimated to be $74.24 for the airline in 2019. The study attempts to tackle the problem by building an end-to-end machine learning pipeline using PySpark on Databricks to predict flight delays. 

## Notebooks & Process

The five notebooks with complete source codes can be found using the links below:

- **Master** ([HTML](https://yintrigue.github.io/ml_flight_delays/src/html/fp_model_master.html), [IPYNB](https://yintrigue.github.io/ml_flight_delays/src/fp_model_master.ipynb)) includes the end-to-end pipeline.
- **EDA** ([HTML](https://yintrigue.github.io/ml_flight_delays/src/html/fp_eda.html), [IPYNB](https://yintrigue.github.io/ml_flight_delays/src/fp_eda.ipynb)) includes the EDA prior to data engineering and model building.
- **Data Cleaning/Join** ([HTML](https://yintrigue.github.io/ml_flight_delays/src/html/fp_data_cleaning_join.html), [IPYNB](https://yintrigue.github.io/ml_flight_delays/src/fp_data_cleaning_join.ipynb)) includes the cleaning and joining of the two primary datasets, Airlines (1GB) and Global Weather (25GB).
- **GBT Toy Example** ([HTML](https://yintrigue.github.io/ml_flight_delays/src/html/fp_toy_ex.html), [IPYNB](https://yintrigue.github.io/ml_flight_delays/src/fp_toy_ex.ipynb)) is an attempt to demonstrate the math behind Gradient Boosted Tree (GBT) using a simple NumPy example. 

The end-to-end training pipeline built for the study is summarized as follow:

![workflow](https://www.dropbox.com/s/tgmv2b2kn0pdfh0/pipeline.png?raw=1) 

## Problem Statements

## Datasets

## Evaluation

## Feature Engineering

## Models 

## Results

## Future Improvements

​    

## Repository 
- [`paper`](./paper) includes our current versions of the research paper. We are currently in the process of refining the research in response to feedback from ACL submission.
- [`src`](./src) includes the notebook with all the source codes for modeling and training.
- `data` includes the datasets we used for training NT5.
- `error_analysis` includes a sample of the reports used to evaluate NT5’s performance.
- `models` includes a sample NT5 model.
- `tfrec` includes the source codes used to generate the TFRecord files used for data streaming during training.

