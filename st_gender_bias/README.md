# Gender Bias in Auto Repair Pricing  
**Keywords**: Randomized Field Experiment, 2x2 Factorial Design, Blocking, Power Analysis, OLS, ANOVA  
**Tech Stack**: R  

*Gender Bias in Auto Repair Pricing* is an end-to-end research project ([paper can be found here](./paper_gender_bias.pdf)) that includes a **randomized field experiment**. Multiple other academic researches on similar topics have been conducted. One study that closely relates to our research is [Repairing the Damage: The Effect of Price Knowledge and Gender on Auto Repair Price Quotes](https://www.nber.org/system/files/working_papers/w19154/w19154.pdf), a 2013 field experiment by Busse, Israeli, and Zettelmeyer that examined whether perceptions about women’s knowledge of market prices drives gender discrimination. They found that when customers signalled unfamiliarity with market rates, **women were quoted $23 more**, on average, than men. Interestingly, they also found that shops were **more likely to provide a discount when asked by a female** **caller**.

## Research Question

Our research question is: **Does a caller's gender influence auto repair price quotes?** We also examine the interaction between caller gender and English as a second language (ESL) status. To build an achievable scope, our experiment is limited to quotes on replacing the **radiator for a 2012 Toyota Camry LE**, and auto shops in the top 25 cities by population within the **Washington state**. The detailed phone script can be found in *Appendix A: Caller Script* in the [paper](./paper_gender_bias.pdf).

## Experiment Design

### Workflow

The study involves a field experiment from end to end. The overall workflow summarized below include three phases: **Experiment Design** (research and experiment setup), **Data Collection** (pilot and data collection/engineering), and **Modeling** (model building and interpretation). In particular, we spent a considerable amount of time on data collection which involves completing a pilot study and assembling a team of **8 callers making a total of 615 calls** to auto shops across the Washington state.

![Workflow](https://www.dropbox.com/s/245fzmcq6q4cfqu/flow.jpeg?raw=1)

### Randomization

The randomization starts with scraping data from Yelp. After removing and filtering (e.g. shops that go out of the business or do not service radiators), we end up a list of 615 auto shops from the top 25 cities by population in the **Washington state**. Note that our sample include **only the shops from the first 4 pages of search results on Yelp**, sorted by user reviews for each city. The decision is mainly due to the limited time and resources available for the experiment, and the focus on top ranking shops by quality, proxied by user reviews on Yelp, should be noted while interpreting the results.

We assemble a team of **8 callers**, which allows us to randomize on two treatment variables: caller **gender**, and **ESL status** (English as a Second Language). The 8 callers are divided into 4 teams, each led by a different researcher on the administration team.

| Caller ID | Gender | ESL Status             | Team |
| --------- | ------ | ---------------------- | ---- |
| 1         | Male   | English Native Speaker | A    |
| 2         | Male   | English Native Speaker | B    |
| 3         | Male   | ESL                    | C    |
| 4         | Male   | ESL                    | D    |
| 5         | Female | English Native Speaker | A    |
| 6         | Female | English Native Speaker | B    |
| 7         | Female | ESL                    | C    |
| 8         | Female | ESL                    | D    |

### Measurement

Our primary outcome variable is the **price quote** received, which directly answers and measures our primary research hypotheses: 

- Female callers on average would receive a higher quote than do male callers
- Female callers who don't speak English natively would on average would receive an even higher quote than female English speakers with no foreign accent. 

In addition, we build in our **mediation analysis** into the experiment design and ask if there are simplicity factors that would cause female and ESL callers to receive higher quotes. The two concepts that measure our hypotheses on mediation are **knowledge** and **respect**, which are proxied by:

-  **Script Knowledge**: Does the caller get questioned about his/her knowledge on the radiator?
- **Quote Breakdown**: Does the caller receive a detailed price breakdown?
- **Attrition**: Does the auto shop refuse or fail to provide a quote?

## Data Collection

We sped a considerable amount of our time collecting data and resolving the various unexpected issues calling the shops. For example, all teams experience relatively low "success" rates at ~50% due to attrition (e.g. shops that answer our calls but refuse/fail to provide a quote) and "non-starters" (e.g. shops that fail to receive treatment by not answering our calls). **Attrition** is fully disclosed with detailed breakdowns in the paper and addressed in modeling using **extreme bounds analysis**. "**Non-starters**," on the other hand, are excluded from modeling but an analysis on their distribution is included in the paper to evaluate the potential **risk of bias**. 

![Data Collection](https://www.dropbox.com/s/6yd7cj6ra6whiyk/data.png?raw=1)

## Results Summary
To avoid **multiple comparisons** (i.e. fishing for significance), we determine the model specifications before running the actual regressions with real data in R. Our model analysis consists of three parts: **Primary Outcome** (price quote), **Secondary Outcomes** (knowledge and respect), and Fun Models (which we build for findings unrelated to the research question).   

Across the four primary and three secondary models, we conclude that:

- Prices received by female callers are different from those received by male callers. **Female callers generally receive a discount** but the prices increase when the quote is given by a female shop representative. 
- We suspect that the price increase from gender affinity for female callers is a result of **female shop representatives being more conservative** on estimates in general. The behavior is evidenced that male callers also receive quotes that are on average $43.95 higher when the shop representatives are female. 
- **ESL callers tend to receive a discount**, but the effect is independent of caller gender with no significant interaction.
- **Female callers were questioned 10% more frequently about their knowledge** about the radiator or car in general compared to male callers. 

### Primary Outcomes

Overall, **R<sup>2</sup> is low** across all four models, suggesting that there are other factors causing the price differences received by our callers. While the experiment setup allows us to focus on just the two randomized variables, caller gender and ESL status, it should be noted that gender and/or ESL only account for a small portion of the variances in pricing, even if they are detained statistically significant. The issue of **gender bias might not be relevant** if the focus is on why prices on auto repairs are different instead of gender inequality. 

Without controlling for the fixed effects (i.e. blocked on “county” and “shop chain”), **Model 1** shows an ATE of -\$40.254 between the treatment and control groups. **Model 2** controls for the fixed effects and the coefficient of the treatment variable stays relatively the same with a slightly lower standard error. Both models suggest that **female callers in our experiment receive a slight discount of roughly \$40**. However, in **Model 3**, the treatment effects for both gender and caller ESL status become insignificant after controlling for the caller’s ESL status and the interaction term. This is evidence that a portion of the variance explained by gender in Model 1 can in fact be explained by the caller’s ESL status. 

**Model 4** includes our two randomized variables (gender and ESL), affinities, and the interaction terms between gender and three other independent variables. Note that our two randomized variables become statistically significant after including the new independent variables and interaction terms. This is a sign of "**negative confounders**," meaning the addition of a covariate (i.e. "removing" the effect of the covariate on outcome from treatment, similar to blocking) results in a "cleaner" treatment that is statistically significant. The interpretation of this rather complicated model is detailed in the paper, but below are a few highlights:

- Being a female or ESL caller generally leads to a deeper discount compared to being a male, non-ESL caller. 
-  ESL callers also tend to receive a discount, but the effect is independent of the caller gender with no significant interaction.
- The affinity factors, contrary to our expectation, do not result in further discounts for female callers. Male callers, on the other hand, do seem to receive some discounts as a result of affinity. The effect pf the two observations, however, can be explained by a behavior unrelated to our research question: Female shop representatives are in general more conservative in their estimates without seeing the actual vehicle.

![Primary Models](https://www.dropbox.com/s/5xb34j05n6hrzcz/models_primary.png?raw=1)

### Secondary Outcomes

"Script Knowledge" measures the stereotype categorical bias that female customers are in general less knowledgeable about cars. The outcome variable is binary with 1 indicating that the caller was questioned about their knowledge according to the different scenarios detailed in Appendix A: Caller Script in the paper. "Attrition" and "Quote Breakdown," on the other hand, are proxies for the shop representative's respect towards the calling customers.

Of the three models, we observe that **female callers were questioned 10% more frequently** about their knowledge about the radiator or car. The finding is rather unexpected because we expect the price to increase when the caller is stereotyped as “less knowledgeable,” but our primary models show that female callers in the experiment actually receive a discount. One possible explanation is that the auto shops we called are honest and refuse to take advantage of a less knowledgeable customer.

<p align="center"><img src="https://www.dropbox.com/s/mqcdkjx2x80oleb/models_secondary.png?raw=1" width="700"/></p>

## Repository 

- [`./paper_gender_bias.pdf`](./paper_gender_bias.pdf) is the paper writeup for the experiment.
- [`./src/models.Rmd`](./src/models.Rmd) includes the models built for the experiment. 
- [`./src/power_analysis.Rmd`](./src/power_analysis.Rmd) includes the power analysis conducted based on the pilot study.
- [`./src/`](./src) contains the source codes for the experiment (data parsing, feature engineering, model building, etc.)
- `./data/` contains the data we scraped and collected for the experiment.