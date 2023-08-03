#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# 
# - In this scenario, I joined a new pharmaceutical company that specializes in anti-cancer medications. Recently, it began screening for potential treatments for squamous cell carcinoma (SCC), a commonly occurring form of skin cancer.The purpose of this study was to compare the performance of Pymaceuticals’ drug of interest, Capomulin, against the other treatment regimens.The executive team has tasked you with generating all of the tables and figures needed for the technical report of the clinical study. They have also asked you for a top-level summary of the study results.
# 
# -Overall, I found that the drug Capomulin has a strong correlation between weight and tumor size in mice studied. 
#  

# In[182]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np

# Study data files
mouse_metadata_path = "Mouse_metadata.csv"
study_results_path = "Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame and Display the data table for preview
mouse_metadata_complete_df = pd.merge(study_results, mouse_metadata, how="left", on=["Mouse ID"])
mouse_metadata_complete_df.head()


# In[87]:


# Checking the number of mice.
#note: I worked with Beatrice from class on this portion
mouse_count = mouse_metadata["Mouse ID"].value_counts()
number_of_mice = len(mouse_count)
number_of_mice


# In[88]:


# Our data should be uniquely identified by Mouse ID and Timepoint
# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
duplicate_mice_ID = mouse_metadata_complete_df.loc[mouse_metadata_complete_df.duplicated(subset=['Mouse ID', 'Timepoint']),'Mouse ID'].unique()
duplicate_mice_ID


# In[89]:


# Optional: Get all the data for the duplicate mouse ID. 
duplicate_mice = mouse_metadata_complete_df.loc[mouse_metadata_complete_df["Mouse ID"] == "g989"]
duplicate_mice


# In[90]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
#note: I used the discussion in https://stackoverflow.com/questions/14057007/remove-rows-not-isinx 
#for this section, and worked with TA Mark
unduplicated_df = mouse_metadata_complete_df[mouse_metadata_complete_df["Mouse ID"].isin(duplicate_mice_ID)==False]
unduplicated_df


# In[91]:


# Checking the number of mice in the clean DataFrame.
unduplicated_mice = unduplicated_df["Mouse ID"].nunique()
unduplicated_mice


# ## Summary Statistics

# In[92]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen
# Use groupby and summary statistical methods to calculate the following properties of each drug regimen: 
# mean, median, variance, standard deviation, and SEM of the tumor volume. 
# Assemble the resulting series into a single summary DataFrame.

#note: I used https://docs.python.org/3/library/statistics.html to find the math functions,
# and the definition of SEM from https://www.sportsci.org/resource/stats/meansd.html
mean = unduplicated_df['Tumor Volume (mm3)'].groupby(unduplicated_df['Drug Regimen']).mean()
median = unduplicated_df['Tumor Volume (mm3)'].groupby(unduplicated_df['Drug Regimen']).median()
variance = unduplicated_df['Tumor Volume (mm3)'].groupby(unduplicated_df['Drug Regimen']).var()
stdev = unduplicated_df['Tumor Volume (mm3)'].groupby(unduplicated_df['Drug Regimen']).std()
SEM = unduplicated_df['Tumor Volume (mm3)'].groupby(unduplicated_df['Drug Regimen']).sem()

regimen_summary = pd.DataFrame({
    "mean tumor volume":mean,
    "median tumor volume":median,
    "variance of  tumor volume ":variance,
    "standard deviation of  tumor volume":stdev,
    "SEM of  tumor volume":SEM})
regimen_summary


# In[93]:


# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# and SEM of the tumor volume for each regimen (only one method is required in the solution)
# Using the aggregation method, produce the same summary statistics in a single line
#note: I used https://datagy.io/pandas-groupby-multiple-columns/ to better understand .aggregate
#Discussed with TA Mark
grouped = unduplicated_df.groupby(['Drug Regimen']).aggregate({'Tumor Volume (mm3)':['mean','median','var','std','sem']})
grouped


# ## Bar and Pie Charts

# In[94]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.
mice_count = unduplicated_df["Drug Regimen"].value_counts()
bar_plot = mice_count.plot.bar()
plt.title("# of Observed Mouse Timepoints by Regimen")
plt.xlabel("Drug Regimen")
plt.ylabel("# of Observed Mouse Timepoints")
plt.tight_layout()


# In[95]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using pyplot.
#note: I referenced https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
mice_count = unduplicated_df["Drug Regimen"].value_counts()
Drug_Regimen=mice_count.index.values
mice_timepoints=mice_count.values
plt.bar(Drug_Regimen, mice_timepoints, width = .8)
plt.xlabel("Drug Regimen")
plt.ylabel("# of Observed Mouse Timepoints")
plt.title("# of Observed Mouse Timepoints by Regimen")
plt.xticks(rotation="vertical")
plt.show()


# In[96]:


# Generate a pie plot showing the distribution of female versus male mice using Pandas
#referenced https://www.geeksforgeeks.org/how-to-create-pie-chart-from-pandas-dataframe/
mice_sex_count = unduplicated_df["Sex"].value_counts()
mice_sex_count.plot(kind='pie', y='mice_sex_count', autopct='%1.1f%%')


# In[97]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot
#note: referenced https://www.w3schools.com/python/matplotlib_pie_charts.asp
mice_sex_count = unduplicated_df["Sex"].value_counts()
labels = 'Male', 'Female'
plt.title("Mice Sex Distribution")
plt.pie(mice_sex_count, labels=labels,autopct='%1.1f%%')
plt.show()


# ## Quartiles, Outliers and Boxplots

# In[98]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin
# Start by getting the last (greatest) timepoint for each mouse

mouse_max_timepoint = mouse_metadata_complete_df.groupby('Mouse ID').max()['Timepoint']
mouse_max_timepoint

# Merge this group df with the original DataFrame to get the tumor volume at the last timepoint

last_tumor_df = pd.merge(mouse_max_timepoint, unduplicated_df, on=("Mouse ID","Timepoint"),how="left")
last_tumor_df

#note: I found out how to do multiple options for .loc from https://sparkbyexamples.com/pandas/pandas-loc-multiple-conditions/ . This would narrow down the list already to the drugs
#we wanted, but since it later asks for loops, I removed this, but am keeping it as markup so I can reference this for my own use.
#last_tumor_limited = last_tumor.loc[(last_tumor["Drug Regimen"] == "Capomulin") | (last_tumor["Drug Regimen"] == "Ceftamin") | (last_tumor["Drug Regimen"] == "Ramicane") | (last_tumor["Drug Regimen"] == "Infubinol")]
#last_tumor_limited_df = pd.DataFrame(last_tumor_limited)
#last_tumor_limited_df


# In[109]:


# Put treatments into a list for for loop (and later for plot labels)
treatments = ["Capomulin", "Ramicane", "Infubinol", "Ceftamin"]
# Create empty list to fill with tumor vol data (for plotting)
tumor_vol_data = []

# Calculate the IQR and quantitatively determine if there are any potential outliers. 
# Locate the rows which contain mice on each drug and get the tumor volumes
# add subset 
# Determine outliers using upper and lower bounds
for treatment in treatments:
    treatment_regimen = last_tumor_df.loc[last_tumor_df["Drug Regimen"] == treatment]
    tumor_vol= treatment_regimen['Tumor Volume (mm3)']
    tumor_vol_data.append(tumor_vol)
    
#for Capomulin 
quartile_ca = tumor_vol_data[0].quantile([.25,.5,.75])
lowerq_ca = quartile_ca[0.25]
upperq_ca = quartile_ca[0.75]
IQR_ca = upperq_ca-lowerq_ca
lower_bound_ca = round(lowerq_ca - (1.5*IQR_ca),2)
upper_bound_ca = round(upperq_ca + (1.5*IQR_ca),2)

#for Ramicane
quartile_ra = tumor_vol_data[1].quantile([.25,.5,.75])
lowerq_ra = quartile_ra[0.25]
upperq_ra = quartile_ra[0.75]
IQR_ra = upperq_ra-lowerq_ra
lower_bound_ra = round(lowerq_ra - (1.5*IQR_ra),2)
upper_bound_ra = round(upperq_ra + (1.5*IQR_ra),2)

#for Infubinol
quartile_in = tumor_vol_data[2].quantile([.25,.5,.75])
lowerq_in = quartile_in[0.25]
upperq_in = quartile_in[0.75]
IQR_in = upperq_in-lowerq_in
lower_bound_in = round(lowerq_in - (1.5*IQR_in),2)
upper_bound_in = round(upperq_in + (1.5*IQR_in),2)

#for Ceftamin
quartile_ce = tumor_vol_data[3].quantile([.25,.5,.75])
lowerq_ce = quartile_ce[0.25]
upperq_ce = quartile_ce[0.75]
IQR_ce = upperq_ce-lowerq_ce
lower_bound_ce = round(lowerq_ce - (1.5*IQR_ce),2)
upper_bound_ce = round(upperq_ce + (1.5*IQR_ce),2)
  
#   print(f"For {treatments[0]} values below {lower_bound0} and above {upper_bound0} could be outliers")
print(f"For {treatments[0]} values below {lower_bound_ca} and above {upper_bound_ca} could be outliers")
print(f"For {treatments[1]} values below {lower_bound_ra} and above {upper_bound_ra} could be outliers")
print(f"For {treatments[2]} values below {lower_bound_in} and above {upper_bound_in} could be outliers")
print(f"For {treatments[3]} values below {lower_bound_ce} and above {upper_bound_ce} could be outliers")    


# In[111]:


# Generate a box plot that shows the distrubution of the tumor volume for each treatment group.
flierprops = dict(marker='o', markerfacecolor='r', markersize=12,
                  linestyle='none')
fig1, ax1 = plt.subplots()
ax1.set_title('Tumor growth by treatment')
ax1.set_ylabel('Growth (mm3)')
ax1.set_xlabel("Drug Regimen")
ax1.boxplot(tumor_vol_data, flierprops = flierprops, labels = treatments)
plt.show()


# ## Line and Scatter Plots

# In[119]:


# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin
ca_mice = unduplicated_df.loc[unduplicated_df["Drug Regimen"] == "Capomulin"]
ca_mice.value_counts("Mouse ID")

#select mouse 1509
mouse_1509 = unduplicated_df.loc[unduplicated_df["Mouse ID"] == "l509",:]

#define variables
x_time = mouse_1509["Timepoint"]
y_tumor = mouse_1509["Tumor Volume (mm3)"]

#define the line
plt.plot(x_time, y_tumor)

#add labels
plt.title( "Capomulin treatment of mouse 1509")
plt.xlabel("Timepoint (Days)")
plt.ylabel(" Tumor volume (mm3)")
plt.show()


# In[137]:


# Generate a scatter plot of mouse weight vs. the average observed tumor volume for the entire Capomulin regimen
ca_group = ca_mice.groupby(["Mouse ID"]).mean()

avg_tumor_vol = ca_group["Weight (g)"]
avg_weight = ca_group["Tumor Volume (mm3)"]

plt.scatter(avg_tumor_vol, avg_weight)
plt.title('Mouse Weight Versus Average Tumor Volume')
plt.xlabel('Weight (g)',fontsize =12)
plt.ylabel('Average Tumor Volume (mm3)')


# ## Correlation and Regression

# In[181]:


# Calculate the correlation coefficient and a linear regression model 
# for mouse weight and average observed tumor volume for the entire Capomulin regimen
#create the starting scatter plot (same as before)
ca_group = ca_mice.groupby(["Mouse ID"]).mean()

avg_tumor_vol = ca_group["Weight (g)"]
avg_weight = ca_group["Tumor Volume (mm3)"]

plt.scatter(avg_tumor_vol, avg_weight)
plt.title('Mouse Weight Versus Average Tumor Volume')
plt.xlabel('Weight (g)',fontsize =12)
plt.ylabel('Average Tumor Volume (mm3)')

#calculate relevant items for regression modeling
#correlation efficient
corr=round(st.pearsonr(avg_weight,avg_tumor_vol)[0],2)
print(f"The correlation between mouse weight and average tumor volume is {corr}")

#calculate slope, and determine regression line
x_values = avg_tumor_vol
y_values = avg_weight

(slope, intercept, rvalue, pvalue, stderr) = st.linregress(x_values, y_values)
regress_values = x_values * slope + intercept

line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
print(f"The Regression line is modeled by the equation {line_eq}")
plt.plot(x_values,regress_values,"r-")

