# Predicting Flight Delays

**Final Model**: Gradient Boosted Tree  
**Baseline Models**: XGBoost Tree, Random Forest, Logistic Regression, SVM   
**Tech Stack**: PySpark, Scikit-learn, Databricks, AWS, Distributed Computing     

Flight delays are costly — the delay cost per minute was estimated to be $74.24 for the airline in 2019. The study attempts to tackle the problem by building a **distributed machine learning pipeline** using PySpark to predict flight delays. The final model is trained on an AWS cluster with **five r4.xlarge nodes** through Databricks. 

## Notebooks & Training Pipeline

The contents in README only briefly describe the high-level methodology. For a detailed writeup, please refer to the **five notebooks** below with complete source codes:

- [**Master Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_model_master.html) includes the writeup and source does for the entire pipeline from end to end.
- [**EDA Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_eda.html) includes the 18 EDAs prior to data engineering and model building.
- [**Data Cleaning/Join Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_data_cleaning_join.html) includes the source codes and detailed description on how the 5 datasets are cleaned, verified, and joined.
- [**GBT Toy Example Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_toy_ex.html) is an attempt to demonstrate the math behind Gradient Boosted Tree (GBT) using a simple NumPy example. 

The end-to-end training pipeline built for the study is summarized as follow:

![workflow](https://www.dropbox.com/s/tgmv2b2kn0pdfh0/pipeline.png?raw=1) 

## Challenges

Flight prediction presents a number of key challenges:

- **Parallel Computing**: The sheer size of the data demands distributed data processing and training. The pipeline was built and run on a cluster of **five r4.xlarge nodes** (1 driver and 4 workers), each with 4 cores and 30.5 GB of memory . 
- **Data Leakage**: Data leakage (using future data to predict past flights) is major issue due to the the time series nature of our two primary datasets: Airlines and Global Weather. Multiple measures have been built in to the pipeline to prevent data leakage during training.
- **Imbalanced Dataset**: Only 20% of the examples are positive. This has a significant impact on how we choose the metrics and training methodology. 
- **Real-world Datasets**: The five datasets are sourced directly from five different organizations. They come with lots of noise and require a considerable amount of cleaning and joins before they can be fed to the pipeline.   
- **Open-ended Objective**: While the goal is to predict flight delays, multiple key questions remain open at the beginning of the project: How should we define a delay? Who are the customers and what are their use cases? How should we evaluate our model?  

## Problem Statements

A flight delay can impact at least three key stakeholders: airlines, airports, and passengers. Each stakeholder can have a different requirement and tolerance for **false positive/negative** predictions. For example, an airline can have a much lower tolerance for false negative than an average passenger if its priority is to improve customer ratification rather than operational costs. 

![Delay Cost Analysis](https://www.dropbox.com/s/v26wjzt1yqp0vm9/delay_cost_small.png?raw=1)

In this study, we envision ourselves as a startup solving the problem of flight delays. Our goal is to predict a flight's **departure delay**, with a threshold of **15 minutes.** A flight's departure is deemed "delayed" if its departure time is 15 minutes or later than its original schedule. The justification for the 15-minute threshold is twofold: 

- As a startup, we aim to build a generic baseline model that can be further fine-tuned according to client requests. 
- 15 minutes is the industry standard, allowing us to easily communicate results to the clients and compare our model's performance to the current SOTAs.

Note that the prediction is done **2 hours** ahead of the flight's scheduled departure time, which has an important implication on feature engineering including the prevention of **data leakage** (i.e. using future data to predict past delays). 

## Performance Evaluation

Our prediction task is a binary classification, with 1 indicating "15-minute delay" and 0 indicating "on-time." Our primary metric is **F0.5**, with **PR AUC** as a secondary metric throughout the training. F0.5 allows us to **prioritize precision over recall**. We aim for a high precision so that our client can feel confident about taking actions based on our predicted delays, even when they know that our model is unable to pick up all delays.

## Datasets

Our training leverages a total of five datasets from multiple sources:  
- **Airlines** from BTS includes statistics about a total of 31,746,841 domestic flights in the US from 2015 to 2019.
  - Size: ~1GB
  - Source: Airline On-Time Performance Data from BTS, [https://tinyl.io/3cx9](https://tinyl.io/3cx9)
- **Global Weather** from NCEI includes historical weather data with 630,904,436 entries across the globe from 2015 to 2019. 
  - Size: ~25GB
  - Source: Global Integrated Surface Dataset from NCEI, [https://tinyl.io/3cSL](https://tinyl.io/3cSL) | [https://tinyl.io/3iIG](https://tinyl.io/3iIG)
- **Weather Stations Metadata** from NCEI includes the metadata about the weather stations where the weather data from NCEI are collected. 
  - Size: ~340KB
  - Source: Master Station History Report from NCEI, [https://tinyl.io/3cSk](https://tinyl.io/3cSk)
- **Airport Coordinates** from BTS includes the coordinates of all airports in the US.
  - Size: ~743KB
  - Source: Aviation Support Master Coordinate from BTS, [https://tinyl.io/3cSb](https://tinyl.io/3cSb)
- **Airport Time Zone** includes the mapping between airports and their respective time zones. 
  - Size: ~180KB
  - Source: Datuetil, [https://tinyurl.com/yhmy5bz2](https://tinyurl.com/yhmy5bz2)

## Data Join

The five datasets are joined after basic cleaning prior to feature engineering. Due to the sheer size of Airlines and Global Weather datasets, extra attention is paid to the **time/space complexity** for the join. Our workflow for the join is summarized below. The final join between the two largest datasets takes roughly 5 minutes and the overall storage space required reduces from 26GB+ to 3.46GB. A more detailed description for the flow is included later in the [EDA notebook](https://yintrigue.github.io/ml_flight_delays/src/html/fp_eda.html).

![Joining Airlines & Weather](https://www.dropbox.com/s/k4k15vzc33a030m/join.png?raw=1)

## Data Split

To prevent data leaks (i.e. using future data to predict past data), we employ the following steps: 

- **2019** is reserved as the test dataset.
- **2071/2018** are used as the training/validation sets respectively for:
  - Training the baseline models; and
  - Fine-tuning the model hyperparameters with random search
- With the fine-tuned hyperparameters, the number of years to be used for training the final model is then determined using an exhaustive grid-search.

<p align="center"><img src="https://www.dropbox.com/s/2j6sfe4ycuccuje/split.png?raw=1" width="800"/></p>

## EDA

The [EDA notebook](https://yintrigue.github.io/ml_flight_delays/src/html/fp_eda.html) includes **18 EDAs** that provide important inputs to our feature engineering/selection and model training/fine-tuning. Our EDAs are separated into four broad categories: Datasets, Airlines, Airports, and Weather. In particular, **two key lessons** have a significant impact on our feature engineering: 

- Delays propagate through time (e.g. if a flight departs late, it arrives late).

<p align="center"><img src="https://www.dropbox.com/s/qo3k9avwzvde6mg/eda_1.png?raw=1" width="600"/></p>

- Delays are highly seasonal, even by hours of a day. 

<p align="center"><img src="https://www.dropbox.com/s/dzvn0mhzkvx3hcf/eda_2.png?raw=1" width="750"/></p>

Based on the two key lessons, many of our features are built on the hypothesis that **a delay is best predicted by another delay**. 

## Feature Engineering

We spent a good portion of our time brainstorming, building, and testing new features. The **41 features** that we build and experiment with fall into 6 different buckets:  

<p align="center"><img src="https://www.dropbox.com/s/5d8hq99rief4gdr/features.png?raw=1" width="900"/></p>

Given the time series nature of the flights data, a **major challenge** with the project is to prevent **data leakage through time** (predicting current flights using future data).  For example, not all features in the Airlines dataset can be used if the flight arrives between the predication time and 15 minutes prior to the prediction time, as shown by the diagram below. All features built require us to carefully think through the possible scenarios in order to prevent leakage. 



<p align="center"><img src="https://www.dropbox.com/s/s1w8vm74o75p81c/delay_02.png?raw=1" width="600"/></p>

We also build in a "**leakage sanity check**" in our process using the **WOE** (Weight of Evidence) and **IV** (Information Value) associated with our custom-built features. Any feature with an IV score much larger than 0.5 is suspicious and subject to investigation on data time leakage. 

In addition, we use WOE and IV for **feature selection**. A feature with a higher IV is an indication of a stronger predictive power. However, features with low IVs are not necessarily always "useless" because they could still be included in the model for explaining a different portion of the label variance. The equations for WOE/IV and an IV plot for our final model are shown below. 

<p align="center"><img src="https://www.dropbox.com/s/uswjx3u0oel5khj/woe.jpg?raw=1" width="300"/></p>

<p align="center"><img src="https://www.dropbox.com/s/iwo5rrruqlfo7qs/woe2.jpg?dl=1" width="500"/></p>

  

![IV](https://www.dropbox.com/s/4rbue6inzggle67/wow_plot.jpg?raw=1)


## Model Selection 

**Four baseline models** are explored in this section: Logistics Regression (LR), Support Vector Machine (SVM), Random Forest (RF), and Gradient Boosted Tree (GBT). The performance using **6 months of data** (Oct/Nov/Dec from 2018 for training and Oct/Nov/Dec from 2017 for validation) are summarized below.

|             |     LR 	|     RF 	|    GBT 	|    SVM 	|
| ---- | ---: | ---: | ---: | ---: |
| **F0.5 Score** | 0.4172 	| 0.4499 	| 0.4763 	| 0.3763 	|
| **Recall** | 0.6411 	| 0.1793 	| 0.6463 	| 0.6584 	|
| **Precision** | 0.3837 	| 0.7223 	|  0.447 	| 0.3399 	|
| **Accuracy** | 0.7707 	| 0.8531 	| 0.8095 	| 0.7133 	|
| **Training Time (Minute, 3-Month Data)** |   1.88 	|   3.43 	|   4.21 	|   2.38 	|

Our **model selection** is based on the following criteria:

- **Performance**: How much room is there for further performance improvement?
- **Efficiency**: What is the time/space complexity for training and predication?
- **Scalability**: Is the model capable of scaling up with up to 3 to 4 full years of training data? 
- **Interoperability**: Can the model provide feedback that allow us to fine-tune the performance?

 **GBT** is our final model. Detailed justification is described in the Baseline Models section in the Master notebook, but the overall selection process is as follows:

![Model Select](https://www.dropbox.com/s/92y2v0dvsbrsgxr/model_select.png?dl=1)  

- **Interpretability**: Linear SVM is first excluded because the model is not probabilistic and does not provide a straightforward way to compute PR AUC and fine-tune on classification probability. 
- **Performance**: LR is excluded because we suspect that our data are not linearly separable, as evidenced by the relatively poor performance of the LR baseline model. Fine-tuning a LR model in our case could take more efforts than a tree mode. 
- **Performance-Efficiency Tradeoff**: RF is embarrassingly parallel while GBT is known to generally perform better (possibly because RF reduces error by reducing variance while GBT reduces errors by both bias and variance). Between the two models, our final choice is GBT given our priority of performance over efficiency. 

## Fine-Tuning  
The fine-tuning process consists of three sequential stages:

<p align="center"><img src="https://www.dropbox.com/s/z7tmkf1relenwvs/finetune.png?dl=1" width="800"/></p>

- Fintuning GBT's **hyperparameters** using k-fold cross-validation. 
- Fine-tuning the **number of years** of training data for the final model. We hypothesize that more years of training data do not necessarily translate to a better performance. The older the data are (e.g. 2015) the less relevant it becomes for predicting the current year (e.g. 2019).
- Fine-tuning the **classification probability threshold** by examining the PR curve.

Note that the hyperparameters are fine-tuned using the **k-fold walk-forward cross-validation**, as illustrated by the diagram below. The approach is necessary to prevent **data leaks** (e.g. using 2018 data to predict 2017 flights).

<p align="center"><img src="https://www.dropbox.com/s/vy437ei09b9crgf/cv.png?raw=1" width="720"/></p>

## Results

Our fine-tuned hyperparameters for GBT are shown below:

| Hyperparameter                           | Value |
| ---------------------------------------- | ----- |
| Max Iteration                            | 64    |
| Max Depth                                | 5     |
| Max Bins                                 | 256   |
| Step Size (Learning Rate)                | 0.1   |
| Data Scaling                             | False |
| Downsampling Ratio for Negative Examples | 0.4   |
| Classification Threshold                 | 0.8   |

Our final model, optimized for F0.5, achieves an overall **PRAUC of 0.6918** and an **F0.5 score of 0.7020**. This is a significant improvement from the GBT baseline model with a PRAUC of 0.6294 and an F0.5 score of 0.4859. However, our performance on F0.5 and precision comes with a significant cost at the recall score, which is quite low at 0.3749. 

<p align="center"><img src="https://www.dropbox.com/s/ezy0zf0fexzhddw/fm_metrics.png?dl=1" width="300"/></p>

<p align="center"><img src="https://www.dropbox.com/s/zba9ji0jc7x2myg/fm_curves.png?dl=1" width="700"/></p>

<p align="center"><img src="https://www.dropbox.com/s/s1k403po53yp32k/fm_confusion.png?dl=1" width="400"/></p>

The error analysis and proposed future work streams are discussed in the [Master notebook](https://yintrigue.github.io/ml_flight_delays/src/html/fp_model_master.html). One idea we would like to explore but are limited by the time and resources available is a **sequential training pipeline** illustrated as follows. The rationale behind the architecture is that our EDA shows that the four types of delays can exhibit very different behaviors: cancels, diverts, group-12 delays (delays longer than 3 hours), and normal delays (delays between 15 minutes and 3 hours). We hypothesize that a sequential pipeline as such would be **superior** to a single multinomial model because each label demands a complete different training methodology given their unique characteristics. 

<p align="center"><img src="https://www.dropbox.com/s/knrxsknu7c5rezy/serial.png?raw=1" width="600"/></p>

## Repository 
- `./src` includes all the notebooks with write-ups and source codes for modeling and training.
  - [**Master Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_model_master.html) includes the writeup and source does for the entire pipeline from end to end.
  - [**EDA Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_eda.html) includes the 18 EDAs prior to data engineering and model building.
  - [**Data Cleaning/Join Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_data_cleaning_join.html) includes the source codes and detailed description on how the 5 datasets are cleaned, verified, and joined.
  - [**GBT Toy Example Notebook**](https://yintrigue.github.io/ml_flight_delays/src/html/fp_toy_ex.html) is an attempt to demonstrate the math behind Gradient Boosted Tree (GBT) using a simple NumPy example. 
- [`./data`](./data) includes the datasets used for the training pipeline.

