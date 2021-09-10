"""
    filename: vaccination.py
    Author: Chien-Chih Wang
    description: REMEMBER TO WRITE
"""
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from components.vaccination_explain import vaccination_explanation

# TODO: write description
# TODO: font family -> 細字 黑體 Myriad Pro 華康中黑體(P)
# TODO: reposition the legend, and the title

############################ settings ############################
# set the page configuration at the beginning, then renders the content
st.set_page_config(layout="wide")

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
  """group the data by location and get last date data
  """
  return dataframe.groupby('location').last().reset_index()

# reference: https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804/2
def local_css(file_name):
  """import the css file, and use markdown to render
  """
  with open(file_name) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_selected_country(select_box):
  return select_box
############################ data parsing ############################

# apply css
local_css("style.css")

# data parsing
# vaccination data
vaccination_data = pd.read_csv('data/vaccinations.csv')
df = pd.DataFrame(vaccination_data)

# imf vaccine secured data
imf_data = pd.read_csv('data/imf-who-covid-19-vaccine-supply-tracker.csv',skiprows=2, engine='python')
df_imf = pd.DataFrame(imf_data)

############################ data section ############################

# """ This section wraps up the data manipulation
# Originally, the data is processed in each section. It could be messy if the chart changes
# orders, which might prone to errors.
# """

# TODO: separate the data manipulation and the webpage layout -> import the variable from the data file

##### choropleth map section #####
# get the newsest date vaccination row by country
country_lastest_vaccination = vaccination_lastest_date_by_country(df)

# get the dataframe for ranking
df_vaccination_by_country = country_lastest_vaccination\
                            .sort_values(by='total_vaccinations_per_hundred', ascending=True)

# group the vaccination rate into different group for 6 classes
df_vaccination_by_country['doses administered per 100 people'] = df_vaccination_by_country\
                                ['total_vaccinations_per_hundred'].apply(group_vaccination)

##### search bar #####
# a list of countries, sorted alphabatically
countries = df_vaccination_by_country.sort_values(by='location')['location'].tolist()

# the selectbox takes the countries list; return a selected country string as a variable
# TODO: how to bring the search bar down without breaking the data order?
selected_country = st.selectbox('', countries, index=countries.index('Taiwan'))

# get the specific country vaccination per hundred; for user interactions
country_vaccination = df_vaccination_by_country\
                      [df_vaccination_by_country['location']==selected_country]\
                      ['total_vaccinations_per_hundred'].values[0]

vaccination_avg = df_vaccination_by_country['total_vaccinations_per_hundred']\
                    .mean().round(decimals=2)

##### vaccination bar chart #####
# rename the column for merging column data from another dataframe
# merge the country name
# for using the same country name across two datasets
df_imf = df_imf.rename(columns={"ISO3":"iso_code"})
df_country = df_vaccination_by_country[['location','iso_code']]
df_imf = df_imf.merge(df_country, on='iso_code', how='inner')

# vaccination calculation
# total doses of vaccination
total_vaccinations = df_vaccination_by_country\
                    [df_vaccination_by_country['location']==selected_country]['total_vaccinations']

# total counts of how many people get vaccinated
people_vaccinated = df_vaccination_by_country\
                    [df_vaccination_by_country['location']==selected_country]['people_vaccinated']

# total counts of how many people get fully protected
people_fully_vaccinated = df_vaccination_by_country\
                          [df_vaccination_by_country['location']==selected_country]\
                          ['people_fully_vaccinated']

# get the specific population of a country
population = df_imf[df_imf['location']==selected_country]['Population']

# for the vaccination chart plotting
data = [total_vaccinations, people_vaccinated,people_fully_vaccinated, population]

##### secured vaccine bar chart #####
# get the fully vaccinated and iso code columns to be merged to another dataset; calculate the ratio
df_people_fully_vaccinated = df_vaccination_by_country[['people_fully_vaccinated','iso_code']]

# merged to the imf dataset
df_imf = df_imf.merge(df_people_fully_vaccinated, on='iso_code', how='inner')

# calculate the fully vaccination rate column value
df_imf['fully_vaccination_rate'] = df_imf['people_fully_vaccinated']/df_imf['Population']

# get the specific country's fully vaccination rate
country_fully_vaccination = df_imf[df_imf['location']==selected_country]\
                              ['fully_vaccination_rate'].values[0]

# format the number to be percent with 4 decimal pricision
country_fully_vaccination = np.round(country_fully_vaccination, decimals=4)*100

# get the rank of fully vaccination rate
df_imf['fully_vaccination_rate rank'] = df_imf['fully_vaccination_rate']\
                                          .rank(method='max')

# get the specific country's fully vaccination rate rank
fully_vaccination_rank = df_imf[df_imf['location']==selected_country]\
                          ['fully_vaccination_rate rank']\
                          .values[0].astype(np.int64)

# rename the column and make the unit consistent
df_imf = df_imf.rename\
          (columns={"Secured Vaccine (millions of courses)": "Secured Vaccine (courses)"})

# unit changes to 1 instead of 1 million
df_imf['secured vaccine per population'] = df_imf["Secured Vaccine (courses)"]\
                                              .apply(lambda x:x*1000000)/df_imf["Population"]

# secured vaccine doses one people could take in their country
# secured vaccine divided by population
vaccine_per_population = df_imf[df_imf['location']==selected_country]\
                          ['secured vaccine per population'].values[0]

# calculate the (secured vaccine)/population rank
df_imf['secured vaccine per population rank'] = df_imf['secured vaccine per population']\
                                                  .rank(method='max')

# get the specific country's secured vaccine per population rank
vaccine_rank = df_imf[df_imf['location']==selected_country]\
                ['secured vaccine per population rank']\
                .values[0].astype(np.int64)

# round the rank to the 2 decimals precision
vaccine_per_population = np.round(vaccine_per_population, decimals=2)

# calculate the total doses per hundred rank
df_vaccination_by_country['total_vaccination_per_hundred rank'] = \
    df_vaccination_by_country['total_vaccinations_per_hundred'].rank(method='max')

# get the specific country's total doses per hundred rank
vaccination_rank = df_vaccination_by_country\
                    [df_vaccination_by_country['location']==selected_country]\
                    ['total_vaccination_per_hundred rank'].values[0].astype(np.int64)

############################ choropleth map section ############################

# title
st.title("COVID-19")
st.title("vaccine doses administered per 100 people")

colors = ['#edf8e9','#c7e9c0','#bae4b3','#74c476','#31a354','#006d2c']

fig_map = px.choropleth\
          (df_vaccination_by_country,
          locations="iso_code",
          color="doses administered per 100 people",
          hover_name="location",
          color_discrete_sequence=colors)
# TODO: consistent font family
fig_map.update_layout(
  legend=dict(
    orientation='h', # type of the legend presented
    title_text="", # not showing the legend title
    itemsizing="trace", # ("trace" | "constant"); trace the graph size and changes
    y=0.11), # adjust the legend y-axis height
  width=1200, height=800, # define map size
  font=dict(
    family="Courier New, monospace",
    size=20,
    color="#7f7f7f"),
  margin=dict(
    l=0, r=0, t=0, b=0), # cut down the margin of the map
  dragmode=False # disable zoom in and out
  )

st.plotly_chart(fig_map)

############################ sidebar section ############################

# TODO: add more pages here
st.sidebar.text("Menu")

############################ vaccination bar chart section ############################

# TODO: rename the label to be without underscore
# TODO: re-design the st.write() text

vaccination1, vaccination2 = st.columns([1,2])

with vaccination1:
  st.title("Select a Country")
  # selected_country = st.selectbox('', countries, index=countries.index('Taiwan'))
  st.text(f"{selected_country} vaccination rate is: {country_vaccination}%")

  st.text(f"The world average: {vaccination_avg}%")

with vaccination2:
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

############################ vaccine secured and ranking section ############################

col1, col2 = st.columns([1,2])

with col1:

  st.title(f'{selected_country} ranking')
  
  st.write(f'secured vaccine: {vaccine_per_population} doses per person')
  st.write(f'rank: {vaccine_rank}')

  st.write(f'vaccination rate: {country_vaccination}%')
  st.write(f'rank: {vaccination_rank}')

  st.write(f'fully vaccination rate: {country_fully_vaccination}%')
  st.write(f'rank: {fully_vaccination_rank}')

with col2:
  # merge the data from owid-covid-data to imf data
  st.title("Secured Vaccine (courses)")

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
  
