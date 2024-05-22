# %%
import pandas as pd
import os

os.getcwd()

# %%
# Load Fatal Encounters data set
fatal_encounters_original = pd.read_csv('fatal_enc.csv')
# Not using other/unknown
fatal_encounters = fatal_encounters_original[fatal_encounters_original['race_imputed'] != 'Other/Unknown']
# fatal_encounters

# %%
# Load all US census tracts
all_tracts = pd.read_csv('all_tracts.csv')
all_tracts.rename(columns = {'NH_BlackE': 'Black', 'NH_WhiteE': 'White', 'Hisp_LatinoE': 'Hispanic/Latino'}, inplace = True)
# all_tracts

# %%
# Total population race 'r'
observed_population_r = all_tracts[['Black', 'White', 'Hispanic/Latino']].sum() / 1e6
# convert to millions
observed_population_r

# %%
# Total population (millions) race 'r' living in quintile 'q'
observed_population_rq = all_tracts.groupby('income_quintile')[['Black', 'White', 'Hispanic/Latino']].sum() / 1e6
observed_population_rq

# %%
# Proportion race 'r' living in income quintile 'q'
observed_proportion_rq = observed_population_rq / observed_population_r
observed_proportion_rq

# %%
############################
# Deaths by race 'r' per year (six years) ####
############################
annual_observed_deaths_r = fatal_encounters['race_imputed'].value_counts() / 6

#######################################
# Deaths by income quintile 'q' per year (six years) ####
#######################################
annual_observed_deaths_q = fatal_encounters['income_quintile'].value_counts() / 6

#####################################################
# Fatal encounter count: race by income quintile ####
#####################################################
annual_observed_deaths_rq = pd.crosstab(fatal_encounters['income_quintile'], fatal_encounters['race_imputed']) / 6
annual_observed_deaths_rq = annual_observed_deaths_rq.reindex(columns = observed_population_r.index)

# %%
#########################
# Column percentages ####
#########################
observed_deaths_col_percent_rq = pd.crosstab(fatal_encounters['income_quintile'], fatal_encounters['race_imputed'], normalize = 'columns') # * 100
# observed_deaths_col_percent_rq

# %%
# Annual fatal encounter rate by race only per one million population (six years in data)
observed_rate_r = annual_observed_deaths_r / observed_population_r
observed_rate_r

# %%
# Annual fatal encounter rate (r by q) per one million population (six years in data)
observed_rate_rq = annual_observed_deaths_rq.div(observed_population_rq) / 6
# observed_rate_rq

# %%
#######################################################
# Counterfactual death count based on all races being 
# distributed the same as the white distribution
#######################################################
proportion_adjustment = observed_proportion_rq['White'].values[:, None] / observed_proportion_rq
counterfactual_annual_deaths_rq = proportion_adjustment * annual_observed_deaths_rq
counterfactual_annual_deaths_rq = pd.DataFrame(counterfactual_annual_deaths_rq)
counterfactual_annual_deaths_rq.rename(
    columns = {0: 'Black', 1: 'White', 2: 'Latino'}, 
    # index = {0: 'Q1', 1: 'Q2', 2: 'Q3', 3: 'Q4', 4: 'Q5'},
    inplace = True
)
annual_counterfactual_deaths_r = counterfactual_annual_deaths_rq.sum()
annual_counterfactual_deaths_r

# %%
# Counterfactual rate: annual per 1 million population
counterfactual_rate_r = annual_counterfactual_deaths_r / observed_population_r
counterfactual_rate_r

# %%
# Reduction in rate based on counterfactual distribution
round(1 - counterfactual_rate_r.iloc[[0,2]] / observed_rate_r.iloc[0:2], 4)


