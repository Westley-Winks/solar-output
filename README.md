# solar-output: Project Overview
---
- Created a tool to estimate energy output of a hypothetical solar facility in Central Oregon to allow land owners to assess feasability of putting solar on their property
- Built a client-facing functional report that automatically generates the energy output predictions for the next 7 days using Streamlit
    - Allows for user input via a slider to change the land acreage used for the hypothetical plant
- Optimized random forest model using a grid search cross validation algorithm

## [Demo](https://share.streamlit.io/westley-winks/solar-output/main)
---
<iframe
  src="https://share.streamlit.io/westley-winks/solar-output/main"
  style="width:100%; height:300px;"
></iframe>

## Tools
---
**Packages:** sklearn, streamlit, pandas, requests, matplotlib, numpy

**Environment:** conda, Jupyter, VSCode

## Data
---
- Used feature engineering to transform the target (energy output) to a dimensionless value to allow for scaling to bigger panels
- Used feature selection to select only the most impactful variables

## Model
---
- Tried three different models to decide on the best one (random forest)
    1. Decision Tree
    2. Random Forest*
    3. Multiple Linear Regression
- Used mean average error as a metric
- Used cross validation to avoid overfitting random forest model

## Future Work
---
- try other models (boosted trees like XGBoost, Adaboost, etc.)
- try dropping more unimportant features from random forest model
- integrate hours of sunlight per day into model
- increase prediction time from a week to a month or longer (data dependent)

## References
---
- **Data:** Williams, Jada; Wagner, Torrey (2019), “Northern Hemisphere Horizontal Photovoltaic Power Output Data for 12 Sites”, Mendeley Data, V5, doi: 10.17632/hfhwmn8w24.5
- **Paper:** Pasion, Christil K., 2d Lt, USAF (2019), "MODELING POWER OUTPUT OF HORIZONTAL SOLAR PANELS USING MULTIVARIATE LINEAR REGRESSION AND RANDOM FOREST MACHINE LEARNING"
- **Feature Selection Article:** https://towardsdatascience.com/feature-selection-techniques-in-machine-learning-with-python-f24e7da3f36e