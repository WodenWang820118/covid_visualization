"""
  The file attemps to bring the queries and makes them to
  functions with docstrings. It would at some point simplify
  the layout page code for reading the layout and queries.
"""
import pandas as pd
import streamlit as st
import numpy as np

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
  """group the data by location and get last date data
  """
  return dataframe.groupby('location').last().reset_index()

# reference: https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804/2
def local_css(file_name):
  """import the css file, and use markdown to render
  """
  with open(file_name) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_country_vaccination_rate(df_vaccination_by_country, selected_country):
  """get the specific country's "total_vaccination_per_hundred" from the
  vaccinations data set.
  """
  return df_vaccination_by_country\
          [df_vaccination_by_country['location']==selected_country]\
          ['total_vaccinations_per_hundred'].values[0]

def get_country_vaccination_avg(df_vaccination_by_country):
  """get the average of "total_vaccinations_per_hundred" from the
  vaccinations data set. 
  """
  return df_vaccination_by_country\
          ['total_vaccinations_per_hundred'].mean().round(decimals=2)

def get_total_doses_vaccination(df_vaccination_by_country, selected_country):
  """get the "total_vaccinations" from the vaccinations data set. 
  """
  return df_vaccination_by_country\
          [df_vaccination_by_country['location']==selected_country]\
          ['total_vaccinations']

def get_people_vaccination(df_vaccination_by_country, selected_country):
  """get the "people_vaccinated", which is a number of how many people
  get at least one shot of vaccine, from the vaccinations data set from
  the vaccinations data set.
  """
  return df_vaccination_by_country\
          [df_vaccination_by_country['location']==selected_country]\
          ['people_vaccinated']

def get_fully_vaccination(df_vaccination_by_country, selected_country):
  """get the "people_fully_vaccinated", which is a number of how many
  people get fully protected by the vaccine. For example. two shots of
  BNT, or two shots of AZ, from the vaccinations data set.
  """
  return df_vaccination_by_country\
          [df_vaccination_by_country['location']==selected_country]\
          ['people_fully_vaccinated']

def get_population(df_imf, selected_country):
  """get the specific "population" from the imf-who-covid-19 data set.
  """
  df_imf['Population'].replace(',','', regex=True, inplace = True) # remove comma symbol
  # turn into int64 number type for calculation
  df_imf['Population'] = df_imf['Population'].apply(pd.to_numeric,errors='coerce')
  return df_imf[df_imf['location']==selected_country]['Population']

def get_fully_vaccination_rank(df_imf, selected_country):
  """get the specific country's "full_vaccination_rate rank"
  """
  return df_imf[df_imf['location']==selected_country]\
          ['fully_vaccination_rate rank']\
          .values[0].astype(np.int64)

def secured_vaccine_unit_change(df_imf, selected_country):
  """calculate the number of secured vaccine in to one unit.
  """
  return df_imf[df_imf['location']==selected_country]\
          ['Secured Vaccine (courses)'].apply(lambda x:x*1000000)

def get_vaccination_per_country(df_imf, selected_country):
  """a ratio which how many doses of vaccines provided per person
  """
  return df_imf[df_imf['location']==selected_country]\
          ['secured vaccine per population'].values[0]

def get_vaccination_per_country_rank(df_imf, selected_country):
  """get the specific country's doses per person rank
  """
  return df_imf[df_imf['location']==selected_country]\
          ['secured vaccine per population rank']\
          .values[0].astype(np.int64)

def get_total_vaccination_per_hundred_rank(df_vaccination_by_country, selected_country):
  """get the calculated total vaccination per hundred rank
  """
  return df_vaccination_by_country\
          [df_vaccination_by_country['location']==selected_country]\
          ['total_vaccination_per_hundred rank'].values[0].astype(np.int64)

def get_fully_vaccination_rate(df_imf, selected_country):
  """get the calculated fully vaccination rate
  """
  return df_imf[df_imf['location']==selected_country]\
          ['fully_vaccination_rate'].values[0]