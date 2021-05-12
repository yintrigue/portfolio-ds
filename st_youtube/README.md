# Quality on YouTube Video Popularity  

**Keywords**: OLS, Gauss-Markov Assumptions, Omitted Variable Bias  
**Tech Stack**: R  

## Research Question
Over 720,000 hours of videos are uploaded to YouTube everyday in 2020. The project is a regression analysis from end to end in an attempt to explore the relationship between a video's quality and its popularity one YouTube. In particular, we ask the question: **How does the quality of a video affect its number of views?**  

Note that the regression analysis in this notebook does NOT attempt to establish a causal relationship of any kind due to the lack of a randomized experiment setup. The goal is to analyze the relationship between a video's quality and its popularity on YouTube with a focus is on performing an end-to-end regression analysis including an analysis on the **Gauss–Markov assumptions** and **omitted variable bias**.    

## Dataset 
The dataset consists of **9,489 randomly scraped videos across 17 categories** from YouTube in 2019. The data are compressed into a single csv file amd consists of the following features:
- Video ID
- Uploader Username  
- Age of Video  
- Category  
- Length of Video  
- Views  
- Viewer Rating  
- Number of Ratings  
- Number of Comments  

## Measurements

The operational definitions and relative metrics of the two primary concepts being researched, quality and popularity, are summarized as follows:  

- "**Quality**" is measured by the level of **viewer engagement** the video has attracted. In particular, our primary metric is the video's viewer rating, as specified by the `[rate]` variable in the dataset, although other variables such as the number of comments the video receives are also explored. Note that `[rate]` can be seen as ordinal (because the values of which are not truly continuous), but is assumed continuous throughout the analysis. The potential effect of the assumption is discussed in the conclusion at the end of the report.  
- "**Popularity**" is measured by the **number of views** a video receives. It is the outcome variable of our regression model.  

## Workflow  
The overall workflow is summarized by the flow diagram below. Note that the modeling phase includes a detailed validation on the model by examining the Gauss-Markov assumptions and potential omitted variable biases.  

<img src="https://www.dropbox.com/s/fmpz2ygk9s61hkw/workflow.png?raw=1" width="1100" />

## Results Summary

Multiple EDAs are performed prior to modeling. A rather surprising finding is that there is a **negative correlation between "age" and "number of views"** of the video. initiation suggests that the older videos have more time to attracts views on YouTube. One possible explanation is that videos on YouTube are either "popular" or "dead":

- "Popular" videos tend to continue attracting views until a certain upper limit is reached. The upper bound can be either a "manipulated threshold" set up by YouTube's video ranking algorithm or a result of natural life cycle for the video's popularity.
- "Dead" videos, on the other hand, simply don't attract any significant amount of views no matter how long they live on YouTube.

<img src="https://www.dropbox.com/s/54cciu27f68mhup/eda.png?raw=1" width="480" />

The final model with **robust errors** is summarized as below. A detailed interpretation is included in the Conclusion section in the [notebook](./regression_ytb_qlty_pop.ipynb). Overall, video quality is surprisingly **negatively correlated** with the number of views given our model's specifications: One unit of change in quality, or `[rate]`, would lead to a roughly **-0.156%** change in viewership. 

One possible explanation is that the results are highly **skewed by outliers**: Roughly 15.46% of the videos come with a rating of zero because they have not received any user rating. An important question is why there is an overwhelmingly high number of videos that come with zero rating, and how these zero-rating videos behave comparing to the rest of the video pool on YouTube. The research of the issue could lead us to update our operational definition for the concept, "quality." For example, should we classify a video to be low-quality simply because it fails to show up due to **YouTube's recommendation algorithm**? Unfortunately the dataset given does not contain relevant variables required for the investigation.

<img src="https://www.dropbox.com/s/nveyjd1acqr8iln/model.png?raw=1" width="480"/>

## Gauss-Markov Assumptions

The following four residual plots are referenced by the analysis of the five Gauss-Markov Assumptions plus the residual normality assumption.

<img src="https://www.dropbox.com/s/cntcnuy1t4zeivv/residuals.png?raw=1"/>

**Assumption MLR.1: Linear in Parameters**
While whether the population parameters are truly linear to each other is unknown, the test results and residual plots show evidence that the linear model built in this report is a reasonable estimate for the population.

**Assumption MLR.2: Random Sampling**
We assume Random Sampling for the scope of the analysis. However, the dataset was given, and the assumption of random sampling, as a result, cannot be verified without details on how the data was collected. There is a possibility of clustering due to the unexpected upper bound limit of the `[age]` variable at 1,258 days.  

**Assumption MLR.3: No Perfect Collinearity**
There is no evidence for perfect collinearity despite the fact that multiple variables are highly correlated to each other. The assumption is satisfied.

**Assumption MLR.4: Zero Conditional Mean**
The “Residuals vs. Fitted” plot shows that the residuals roughly have a mean of zero, especially in areas where there is a sufficient amount of data points. The assumption of zero conditional mean is reasonably satisfied.

**Assumption MLR.4': Exogeneity**
No linear relationship is observed in the “Residuals vs. Fitted” plot, which is a positive signal for endogeneity. However, omitted variable bias cannot be verified using residual plots and a detailed analysis of possible omitted variable biases are included in the Omitted Variables section in the [notebook](./regression_ytb_qlty_pop.ipynb).

**Assumption MLR.5: Homoskedasticity**
Both the Scale-Location plot and the Breusch-Pagan test confirm heteroskedasticity. Robust errors are used for the model.

**Assumption MLR.6 Normality**
With the exception for a few outliers, the q-q plot shows a reasonable straight line, which indicates normality. CLT applies because of the large sample size (9443 observations)

## Repository 

- [`./regression_ytb_qlty_pop.ipynb`](./regression_ytb_qlty_pop.ipynb) is the notebook with source codes and writeup for the analysis.
- [`./data_ytb.csv`](./data_ytb.csv) is the raw dataset used for the regression. 

