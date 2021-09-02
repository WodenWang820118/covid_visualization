'''
    filename: vaccination.py
    Author: Chien-Chih Wang
    description: REMEMBER TO WRITE
'''
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from vaccination_explain import vaccination_explanation

############################ settings ############################
# TODO: see the html rendering, then decide what to do with this issue
# set the page configuration at the beginning, then renders the content
# st.set_page_config(layout="wide")

# pylint: disable=W0311
############################ helper functions ############################
# reference: https://waynestalk.com/en/python-choropleth-map-en/
def group_vaccination(vaccination_percentage):
  ''' group the vaccination_percentage into 6 classes '''
  if vaccination_percentage < 40:
    return f'{0}~{40}'
  if vaccination_percentage < 80:
    return f'{40}~{80}'
  if vaccination_percentage < 120:
    return f'{80}~{100}'
  if vaccination_percentage < 160:
    return f'{120}~{160}'
  if vaccination_percentage < 200:
    return f'{160}~{200}'
  return f'{200} above'

def vaccination_lastest_date_by_country(dataframe):
  '''group the data by location and get last date data'''
  return dataframe.groupby('location').last().reset_index()

############################ data parsing ############################

# data parsing
# vaccination data
vaccination_data = pd.read_csv('../data/vaccinations.csv')
df = pd.DataFrame(vaccination_data)

# imf vaccine secured data
imf_data = pd.read_csv('../data/imf-who-covid-19-vaccine-supply-tracker.csv',skiprows=2, engine='python')
df_imf = pd.DataFrame(imf_data)

############################ choropleth map section ############################
# title
st.title("COVID-19 vaccine doses administered per 100 people")

# TODO: highlight the country selected
country_lastest_vaccination = vaccination_lastest_date_by_country(df)
df_vaccination_by_country = country_lastest_vaccination\
                            .sort_values(by='total_vaccinations_per_hundred', ascending=True)

df_vaccination_by_country['doses administered per 100 people'] = df_vaccination_by_country\
                                ['total_vaccinations_per_hundred'].apply(group_vaccination)

custom_data = df_vaccination_by_country['location'].tolist()

colors = ['#edf8e9','#c7e9c0','#bae4b3','#74c476','#31a354','#006d2c']

fig_map = px.choropleth\
          (df_vaccination_by_country,
          locations="iso_code",
          color="doses administered per 100 people",
          hover_name="location",
          color_discrete_sequence=colors)

fig_map.update_layout(autosize=False, width= 1200, height=800)
st.plotly_chart(fig_map)

############################ sidebar section ############################

countries = df_vaccination_by_country.sort_values(by='location')['location'].tolist()

selected_country = st.sidebar\
                    .selectbox('Select a country', countries, index=countries.index('Taiwan'))

country_vaccination = df_vaccination_by_country\
                      [df_vaccination_by_country['location']==selected_country]\
                      ['total_vaccinations_per_hundred'].values[0]

st.sidebar.text(f"{selected_country} vaccination rate is: {country_vaccination}%")

vaccination_avg = df_vaccination_by_country['total_vaccinations_per_hundred']\
                    .mean().round(decimals=2)

st.sidebar.text(f"The world average: {vaccination_avg}%")

############################ bar chart section ############################

# rename the column for merging column data from another dataframe
# merge the country name
df_imf = df_imf.rename(columns={"ISO3":"iso_code"})
df_country = df_vaccination_by_country[['location','iso_code']]
df_imf = df_imf.merge(df_country, on='iso_code', how='inner')

# vaccination calculation
total_vaccinations = df_vaccination_by_country\
                    [df_vaccination_by_country['location']==selected_country]['total_vaccinations']

people_vaccinated = df_vaccination_by_country\
                    [df_vaccination_by_country['location']==selected_country]['people_vaccinated']

people_fully_vaccinated = df_vaccination_by_country\
                          [df_vaccination_by_country['location']==selected_country]\
                          ['people_fully_vaccinated']

population = df_imf[df_imf['location']==selected_country]['Population']

data = [total_vaccinations, people_vaccinated,people_fully_vaccinated, population]

# plot the bar chart
# vaccination based on different definitions of vaccination
individual_data = px.bar(
  data,
  orientation='h',
  text=data)

# chart title
st.title(f'{selected_country} vaccination by different categories')

# chart attributes
individual_data\
  .update_layout(
  yaxis_title=None,
  xaxis_title=None,
  autosize=True,
  margin=dict(l=0,r=0,t=0,b=0),
  width=1000, height=300,
  showlegend=False,
  font=dict(
      family="Courier New, monospace",
      size=18,
      color="RebeccaPurple"
    )
  )
individual_data.update_traces(texttemplate='%{text:,}',marker_color='rgb(158,202,225)')
st.plotly_chart(individual_data)

components.html(vaccination_explanation)

############################ vaccine secured section ############################

st.title("Secured Vaccine (courses)")

df_imf = df_imf.rename\
        (columns={"Secured Vaccine (millions of courses)": "Secured Vaccine (courses)"})

# times 1 million to calcualte the ratio in the same unit
secured_vaccine = df_imf[df_imf['location']==selected_country]\
                  ['Secured Vaccine (courses)'].apply(lambda x:x*1000000)

secured_vaccine_data = [population, secured_vaccine]

# plot the bar chart
secured_vaccine_data_chart = px.bar(
  secured_vaccine_data,
  orientation='h',
  text=secured_vaccine_data)

# chart attributes
secured_vaccine_data_chart\
  .update_layout(
  yaxis_title=None,
  xaxis_title=None,
  autosize=True,
  margin=dict(l=0,r=0,t=0,b=0),
  width=1000, height=170,
  showlegend=False,
  font=dict(
      family="Courier New, monospace",
      size=18,
      color="RebeccaPurple"
    )
  )
secured_vaccine_data_chart\
  .update_traces(texttemplate='%{text:,}',marker_color='rgb(158,202,225)')

st.plotly_chart(secured_vaccine_data_chart)

############################ ranking section ############################

# section title
st.title(f'{selected_country} ranking')

# create 3 columns
col1, col2, col3 = st.columns(3)

##### column 1 #####
with col1:
  df_imf['secured vaccine per population'] = df_imf["Secured Vaccine (courses)"]\
                                              .apply(lambda x:x*1000000)/df_imf["Population"]

  vaccine_per_population = df_imf[df_imf['location']==selected_country]\
                            ['secured vaccine per population'].values[0]

  df_imf['secured vaccine per population rank'] = df_imf['secured vaccine per population']\
                                                    .rank(method='max')

  vaccine_rank = df_imf[df_imf['location']==selected_country]\
                  ['secured vaccine per population rank']\
                  .values[0].astype(np.int64)

  vaccine_per_population = np.round(vaccine_per_population, decimals=2)
  st.write(f'secured vaccine per population: {vaccine_per_population}, rank: {vaccine_rank}')
  # TODO: consistent decimal points and unit

##### column 2 #####
with col2:
  df_vaccination_by_country['total_vaccination_per_hundred rank'] = \
    df_vaccination_by_country['total_vaccinations_per_hundred'].rank(method='max')

  vaccination_rank = df_vaccination_by_country\
                      [df_vaccination_by_country['location']==selected_country]\
                      ['total_vaccination_per_hundred rank'].values[0].astype(np.int64)

  st.write(f'vaccination rate: {country_vaccination}, rank: {vaccination_rank}')

##### column 3 #####
with col3:
  # merge the data from owid-covid-data to imf data
  df_people_fully_vaccinated = df_vaccination_by_country[['people_fully_vaccinated','iso_code']]

  df_imf = df_imf.merge(df_people_fully_vaccinated, on='iso_code', how='inner')

  df_imf['fully_vaccination_rate'] = df_imf['people_fully_vaccinated']/df_imf['Population']

  country_fully_vaccination = df_imf[df_imf['location']==selected_country]\
                                ['fully_vaccination_rate'].values[0]

  country_fully_vaccination = np.round(country_fully_vaccination, decimals=2)

  df_imf['fully_vaccination_rate rank'] = df_imf['fully_vaccination_rate']\
                                            .rank(method='max')
  fully_vaccination_rank = df_imf[df_imf['location']==selected_country]\
                            ['fully_vaccination_rate rank']\
                            .values[0].astype(np.int64)

  st.write(f'fully vaccination rate: {country_fully_vaccination}, rank: {fully_vaccination_rank}')
