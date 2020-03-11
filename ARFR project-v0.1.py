#!/usr/bin/env python
# coding: utf-8

# <h1> ICT Project 1

# <h2> Australian Road Deaths Database (ARDD) 
# <h3>
#     Source: <a href="https://data.gov.au/dataset/ds-dga-5b530fb8-526e-4fbf-b0f6-aa24e84e4277/details?q=road%20crash"> Australia Gov.data.au</a>

# In[8]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[9]:


# ARDD Fatalities
fatalities_url_data = "https://data.gov.au/data/dataset/5b530fb8-526e-4fbf-b0f6-aa24e84e4277/resource/fd646fdc-7788-4bea-a736-e4aeb0dd09a8/download/ardd_fatalities.csv"

df_fatalities_data = pd.read_csv(fatalities_url_data)
df_fatalities_data.head(3)


# In[10]:


# ARDD Fatal Crashes

fatal_crashes_url_data = "https://data.gov.au/data/dataset/5b530fb8-526e-4fbf-b0f6-aa24e84e4277/resource/d54f7465-74b8-4fff-8653-37e724d0ebbb/download/ardd_fatal_crashes.csv"

df_fatal_data = pd.read_csv(fatal_crashes_url_data)
df_fatal_data.rename(columns={'Bus \nInvolvement': 'Bus Involvement'}, inplace=True)

df_fatal_data.head(3)


# In[11]:


# remove rows with missing value in speed limit
df_fatal_data = df_fatal_data[df_fatal_data['Speed Limit'] != '-9']


# In[12]:



# # number of deaths year-wise
# ax = df_fatal_data.plot.bar(x='Crash Type', y='Number Fatalities')
# ax


# In[13]:


df_fatal_data_filtered = df_fatal_data[df_fatal_data['Year']>1985]
piv_deaths = pd.pivot_table(data=df_fatal_data_filtered, values='Number Fatalities', index=['Year'], columns=['Crash Type'], aggfunc='sum')
piv_deaths.head(3)
# piv_deaths = piv_deaths[piv_deaths['Year']==2005]


# In[14]:


ax = piv_deaths.plot(
    kind='bar', 
    stacked=False, 
    color=('#5cb85c', '#5bc0de', '#d9534f'),
    width = 0.8, 
    figsize=(20, 8), 
    legend=True,
    fontsize=14)
ax.set_title("Fatalities over years", fontsize=16)
ax.legend(loc='upper right', frameon=True, fontsize=14)
ax.set_ylabel("# of Fatalities", fontsize=14)
ax.set_xlabel("Year", fontsize=14)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# ax.spines['left'].set_visible(False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




