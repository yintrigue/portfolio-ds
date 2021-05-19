# Promoting Lyft Bay Wheels
**Keywords**: SQL, BigQuery, Plotly, Python  

[Bay Wheels](https://www.lyft.com/bikes/bay-wheels) is a bike rental service of Lyft in the San Francisco Bay Area. The goal of the study is to help the company **increase its commuter ridership** by developing **promotional strategies** based on data analytics. 

The analysis consists of three stages: The concept of a "commuter trip" is first defined. Data analytics are then performed using BigQuery on GCP. Lastly, a total of three strategies are proposed based on the data to increase Bay Wheels' commuter ridership.  

<p align="center"><img src="https://www.dropbox.com/s/bnnkn0nespjh5p3/workflow.png?raw=1" width="600" /></p>

## Datasets

The two datasets, `Bikeshare Trips` and `Bikeshare Stations`, from Bay Wheels are hosted on GCP (Google Cloud Platform) through BigQuery. 

- `Bikeshare Trips` includes a total of **983,648 rental bike trips** over 3 years **from 2013 to 2016**.
- `Bikeshare Stations`, as a complementary dataset, includes **specifications of the stations** (e.g. GPS coordinates, scales, creation/retire dates, etc.) that are owned by Bay Wheels during the same timespan.  

## Concept Definition & Strategic Focuses

A "commuter trip" is roughly defined as **recurring travels** between two distant locations. The *Concept Definition: Commuter Trip* section in the notebook includes a more detailed definition and justification. Note that under the definition, a commuter can be either a subscriber or non-subscriber. 

As our goal is to increase ridership through commuters, our promotional strategies primarily focus on the three stages of the **marketing funnel**, listed in the order of priority:

- **Conversion**: Acquire new customers and convert existing non-subscribers to subscribers.
- **Loyalty**: Increase the ridership of our existing customers.
- **Brand Awareness**: Build brand awareness for new ridership in the long run.

## Recommendation Summary

Given the definition of a commuter, the following three promotional strategies are recommended:

**Recommendation I**: Build subscriber referrals & local partnership programs.

Through data we observe very distinct behaviors between Bay Wheels' subscriber and non-subscribers. For example, we observe that the two types of customers have very different lengths of rental duration. Non-subscribers seem to be renting for leisure instead of commuting.

<p align="center"><img src="https://www.dropbox.com/s/wuf8r4axh7ojuw5/analysis_2.png?raw=1" width=400" /></p>

In addition, the locations where the two types of customers rent bikes are also very different. As shown by the Plotly map below, subscribers concentrate in the downtown area where non-subscribers are mostly renting on specific torts attractions such as the harbors. 


<p align="center"><img src="https://www.dropbox.com/s/65hqu0jayjcw9r8/analysis_1.png?raw=1" width="900" /></p>

Given the very different distinct behaviors, it makes little sense to try converting non-subscribers to subscribers. Most non-subscribers are tourists who rent bikes for fun while visiting the Bay Area. A better strategy is to build **referral programs** to encourage subscribers to attract subscribers, and non-subscribers to attract non-subscribers. **Local partnerships** such as promoting the fun Bay Wheels experience for tourists by partnering with hotels and shops in popular tourist attractions would also be an effective strategy. 

**Recommendation II**: Creating new pricing models for specific routes and low-traffic hours/seasons.

Data show that bike traffic is **highly seasonal** by routes, time of the day, and months. For example, the following three visuals built using by Plotly show the top 100 trips at different times of the day from 2013 to 2016.

<p align="center"><img src="https://www.dropbox.com/s/urddk4gl61ey6bh/analysis_3.png?raw=1" width="900" /></p>

<p align="center"><img src="https://www.dropbox.com/s/xaums04bf1dy8zp/analysis_4.png?raw=1" width="900" /></p>

<p align="center"><img src="https://www.dropbox.com/s/0hj58c4lutg9m95/analysis_5.png?raw=1" width="900" /></p>

Given the seasonal nature of the commuter ridership, we recommend Bay Wheels to develop **custom subscription pricing models** that are route-specific, hour-specific, and even season-specific. For example, Bay Wheels can consider lower the subscription price with the restriction that the subscriber can only rent/return bikes at **certain stations**. A low-priced "**season pass**"  during the winter would also promote the Bay Wheels experience by taking advantage of unused inventory during low-season months. 

**Recommendation III**: Promote great brand stories with inter-area bikers.

While the **median rental hours** for subscribers and non-subscribers are short, at only **1.28 and 8.18 minutes** respectively, we observe  a small number of the bikers who actually use Bay Wheels bikes to travel across a long distance **between the three different regions** in the Bay Area: Palo Alto, Mountain View, Redwood City.  


<p align="center"><img src="https://www.dropbox.com/s/j5jmsm9syth9aq3/analysis_6.png?raw=1" width="400" /></p>

While these bikers are rather rare, we believe that **great brand stories** can be uncovered from these ridership. For example, are tourists (non-subscribers) having fun biking between areas? Or, are some commuters (subscribers) living a healthier lifestyle using Bay Wheels' bikes? These are Bay Wheels' great opportunity to promote the brand through real brand stories!  

## Repository 

- promoting_lyft_bay_wheels.ipynb ([nbviewer](https://nbviewer.jupyter.org/github/yintrigue/portfolio-ds/blob/master/py_lyft_bay_wheels/promoting_lyft_bay_wheels.ipynb.ipynb), [ipynb](./promoting_lyft_bay_wheels.ipynb)) is the notebook with the writeup and source codes.

