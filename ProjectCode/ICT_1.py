#!/usr/bin/env python
# coding: utf-8

# <h1> ICT Project 1

# <h2> Australian Road Deaths Database (ARDD) 
# <h3>
#     Source: <a href="https://data.gov.au/dataset/ds-dga-5b530fb8-526e-4fbf-b0f6-aa24e84e4277/details?q=road%20crash"> Australia Gov.data.au</a>

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium


# In[2]:


# import folium


# In[2]:


aus_geo = r'D:\Downloads\aus.json'

# create a plain world map
latitude = -25
longitude = 125


# In[3]:


# ARDD Fatalities
fatalities_url_data = "https://data.gov.au/data/dataset/5b530fb8-526e-4fbf-b0f6-aa24e84e4277/resource/fd646fdc-7788-4bea-a736-e4aeb0dd09a8/download/ardd_fatalities.csv"

df_fatalities_data = pd.read_csv(fatalities_url_data)
df_fatalities_data.head(3)


# In[4]:


# ARDD Fatal Crashes

fatal_crashes_url_data = "https://data.gov.au/data/dataset/5b530fb8-526e-4fbf-b0f6-aa24e84e4277/resource/d54f7465-74b8-4fff-8653-37e724d0ebbb/download/ardd_fatal_crashes.csv"

df_fatal_data = pd.read_csv(fatal_crashes_url_data)
df_fatal_data.rename(columns={'Bus \nInvolvement': 'Bus Involvement'}, inplace=True)

df_fatal_data.head(3)


# In[5]:


# remove rows with missing value in speed limit
df_fatal_data = df_fatal_data[df_fatal_data['Speed Limit'] != '-9']


# In[6]:


# Dataset filtered with Year > 2015
df_fatal_data_filtered = df_fatal_data[df_fatal_data['Year']>2015]


# In[7]:


# df_fatal_data_filtered = df_fatal_data[df_fatal_data['Year']>2010]
piv_deaths = pd.pivot_table(data=df_fatal_data_filtered, values='Number Fatalities', index=['Year'], columns=['Crash Type'], aggfunc='sum')
piv_deaths.head(3)
# piv_deaths = piv_deaths[piv_deaths['Year']==2005]


# In[9]:


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


# In[10]:


df_fatalities_data_selected = df_fatalities_data[['Crash ID', 'Road User', 'Gender','Age']]
df_fatalities_data_selected


# In[11]:


full_df = pd.merge(df_fatal_data, df_fatalities_data_selected, on='Crash ID', how='left')
full_df.head()


# In[12]:


aus_count = pd.read_csv('D:/Downloads/aus.csv')
aus_count.head()


# In[13]:


df_2019 = full_df[full_df["Year"]==2019]


# In[14]:


df_2019_states = df_2019.groupby('State')


# In[15]:


# df_2019_states
df_2019_states = df_2019_states.count()['Dayweek'].reset_index()


# In[16]:


def state_full_name(state):
    if state == 'NSW':
        return 'New South Wales'
    elif state == 'QLD':
        return 'Queensland'
    elif state == 'Victoria':
        return 'Victoria'
    elif state == 'ACT':
        return 'Australian Capital Territory'
    elif state == 'NT':
        return 'Northern Territory'
    elif state == 'SA':
        return 'South Australia'
    elif state == 'WA':
        return 'Western Australia'


# In[17]:


df_2019_states['Full_state_name'] = df_2019_states['State'].apply(state_full_name)


# In[18]:


df_2019_states.rename(columns={'Dayweek':'Count'}, inplace = True)


# In[19]:


df_2019_states


# In[21]:


aus_map = folium.Map(location=[latitude, longitude], zoom_start=4, tiles='Mapbox Bright')
threshold_scale = np.linspace(df_2019_states['Count'].min(),
                              df_2019_states['Count'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist()     # change the numpy array to a list
threshold_scale[-1] = threshold_scale[-1] + 1  # make sure that the last value of the list is greater than the maximum 


# generate choropleth map using the total count for each state
aus_map.choropleth(
    geo_data=aus_geo,
    name = 'Australia',
    data=df_2019_states,
    columns=['Full_state_name', 'Count'],
    key_on='feature.properties.STATE_NAME',
#     fill_color='YlOrRd', 
    fill_color='YlOrRd', 
    threshold_scale=threshold_scale,
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Australia Fatalities 2015 - 2020',
    reset=True
)

# display map
aus_map


# In[42]:


folium.LayerControl().add_to(aus_map)


# In[ ]:





# In[8]:


df_fatal_data_filtered


# In[61]:


# df_fatal_data_filtered = df_fatal_data[df_fatal_data['Year']>2010]
piv_fatality = pd.pivot_table(data=df_fatal_data_filtered, values='Number Fatalities', index=['Year'], columns=['Crash Type'], aggfunc='sum')
piv_fatality['Total Fatality'] = piv_fatality['Multiple'] + piv_fatality['Pedestrian'] + piv_fatality['Single']
piv_fatality['Multiple'] = round(100 *piv_fatality['Multiple']/piv_fatality['Total Fatality'],2)
piv_fatality['Pedestrian'] = round(100 *piv_fatality['Pedestrian']/piv_fatality['Total Fatality'],2)
piv_fatality['Single'] = round(100 *piv_fatality['Single']/piv_fatality['Total Fatality'],2)
mask = ['Multiple', 'Pedestrian', 'Single']
piv_fatality = piv_fatality[mask]


# In[62]:


piv_fatality.head(3)
# piv_deaths.head(5)


# In[72]:


ax = piv_fatality.plot(
    kind='bar', 
    stacked=False, 
    color=('#5cb85c', '#5bc0de', '#d9534f'),
    width = 0.8, 
    figsize=(20, 8), 
    legend=True,
    fontsize=14)

ax.set_title("Fatalities over years", fontsize=16)
ax.legend(loc='upper right', frameon=True, fontsize=14)
ax.set_ylabel("Fatalities %", fontsize=14)
ax.set_xlabel("Year", fontsize=14)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




