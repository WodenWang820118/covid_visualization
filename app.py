"""
    filename: vaccination.py
    Author: Chien-Chih Wang
    description: REMEMBER TO WRITE
"""

import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from components.vaccination_explain import vaccination_explanation
import utils
import pandas as pd
import numpy as np

# TODO: write description
# TODO: put original dataframe in one of the page

# pylint: disable=W0311

############################ settings ############################
# set the page configuration at the beginning, then renders the content
st.set_page_config(layout="wide")

# check CSS for the font family, font weight, font size and other properties.

############################ data parsing ############################
# data parsing
# vaccination data
vaccination_data = pd.read_csv('data/vaccinations.csv')
df = pd.DataFrame(vaccination_data)

# imf vaccine secured data
imf_data = pd.read_csv('data/imf-who-covid-19-vaccine-supply-tracker.csv',skiprows=2, engine='python')
df_imf = pd.DataFrame(imf_data)

############################ data section ############################

# TODO: the docstrings renders on the webpage. How to disable it?
# """ This section wraps up the data manipulation
# Originally, the data is processed in each section. It could be messy if the chart changes
# orders, which might prone to errors.
# """

##### choropleth map section #####
# get the newsest date vaccination row by country
country_lastest_vaccination = utils.vaccination_lastest_date_by_country(df)

# get the dataframe for ranking
df_vaccination_by_country = country_lastest_vaccination\
                            .sort_values(by='total_vaccinations_per_hundred', ascending=True)

# group the vaccination rate into different group for 6 classes
df_vaccination_by_country['doses administered per 100 people'] = df_vaccination_by_country\
                                ['total_vaccinations_per_hundred'].apply(utils.group_vaccination)

##### search bar #####
# a list of countries, sorted alphabatically
countries = df_vaccination_by_country.sort_values(by='location')['location'].tolist()

# apply css
utils.local_css("style.css")

############################ choropleth map section ############################

st.title("COVID-19")
st.title("vaccine doses administered per 100 people")

colors = ['#edf8e9','#c7e9c0','#bae4b3','#74c476','#31a354','#006d2c']

fig_map = px.choropleth\
          (df_vaccination_by_country,
          locations="iso_code",
          color="doses administered per 100 people",
          hover_name="location",
          color_discrete_sequence=colors)

fig_map.update_layout(
  legend=dict(
    orientation='h', # type of the legend presented
    title_text="", # not showing the legend title
    itemsizing="trace", # ("trace" | "constant"); trace the graph size and changes
    y=0.11), # adjust the legend y-axis height
  width=1200, height=800, # define map size
  font=dict(
    family="Roboto",
    size=20,
    color="#293fe3"),
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

vaccination1, vaccination2 = st.columns([1,2])

with vaccination1:
  st.title("Select a Country")

  selected_country = st.selectbox('', countries, index=countries.index('Taiwan'))
  country_vaccination = utils.get_country_vaccination_rate(df_vaccination_by_country, selected_country)
  vaccination_avg = utils.get_country_vaccination_avg(df_vaccination_by_country)

  ##### vaccination bar chart #####
  # rename the column for merging column data from another dataframe
  # merge the country name
  # for using the same country name across two datasets
  df_imf = df_imf.rename(columns={"ISO3":"iso_code"})
  df_country = df_vaccination_by_country[['location','iso_code']]
  df_imf = df_imf.merge(df_country, on='iso_code', how='inner')

  total_vaccinations = utils.get_total_doses_vaccination(df_vaccination_by_country, selected_country)
  people_vaccinated = utils.get_people_vaccination(df_vaccination_by_country, selected_country)
  people_fully_vaccinated = utils.get_fully_vaccination(df_vaccination_by_country, selected_country)
  population = utils.get_population(df_imf, selected_country)

  # for the vaccination chart plotting
  vaccination_data = [total_vaccinations, people_vaccinated,people_fully_vaccinated, population]

  # TODO: use the mardown to style the text
  vaccination_rate = f"""
  <p class="vaccination-rate"> {selected_country} vaccination rate is: {country_vaccination}% </p>
  <p class="vaccination-avg"> The world average: {vaccination_avg}% </p>
  """
  st.markdown(vaccination_rate, unsafe_allow_html=True)

with vaccination2:
  # plot the bar chart
  # vaccination based on different definitions of vaccination
  individual_data = px.bar(
    vaccination_data,
    orientation='h',
    text=vaccination_data)

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
        family="Roboto",
        size=18,
        color="#293fe3"
      )
    )
  individual_data.update_traces(texttemplate='%{text:,}',marker_color='rgb(158,202,225)')
  st.plotly_chart(individual_data)

  vaccination_explanation = \
  """
  <div>
    <p>
      The <strong>'people_fully_vaccinated'</strong> is the number of whom receive the full protection.
      For example, 1 shot of J&J would be considered as 1. Two shots of Moderna would also be counted as 1.
    </p>
    <p>
      The <strong>'people_vaccinated'</strong> is the number who receive at least one shot of vaccination.
    </p>
    <p>
      The <strong>'total_vaccinations'</strong> is the number total doses of vaccination.
    </p>
  </div>
  """
  st.markdown(vaccination_explanation, unsafe_allow_html=True)

############################ vaccine secured and ranking section ############################

##### secured vaccine bar chart #####
# get the fully vaccinated and iso code columns to be merged to another dataset; calculate the ratio
df_people_fully_vaccinated = df_vaccination_by_country[['people_fully_vaccinated','iso_code']]

# merged to the imf dataset
df_imf = df_imf.merge(df_people_fully_vaccinated, on='iso_code', how='inner')

# calculate the fully vaccination rate column value
df_imf['fully_vaccination_rate'] = df_imf['people_fully_vaccinated']/df_imf['Population']
country_fully_vaccination_rate = utils.get_fully_vaccination_rate(df_imf, selected_country)

# format the number to be percent with 4 decimal pricision
country_fully_vaccination_rate = np.round(country_fully_vaccination_rate, decimals=4)*100

# get the rank of fully vaccination rate
df_imf['fully_vaccination_rate rank'] = df_imf['fully_vaccination_rate']\
                                          .rank(method='max')
fully_vaccination_rank = utils.get_fully_vaccination_rank(df_imf, selected_country)

# rename the column and make the unit consistent
df_imf = df_imf.rename\
          (columns={"Secured Vaccine (millions of courses)": "Secured Vaccine (courses)"})

secured_vaccine = utils.secured_vaccine_unit_change(df_imf, selected_country)

df_imf['secured vaccine per population'] = df_imf["Secured Vaccine (courses)"]\
                                              .apply(lambda x:x*1000000)/df_imf["Population"]

# secured vaccine doses one people could take in their country
# secured vaccine divided by population
vaccine_per_population = utils.get_vaccination_per_country(df_imf, selected_country)

# calculate the (secured vaccine)/population rank
df_imf['secured vaccine per population rank'] = df_imf['secured vaccine per population']\
                                                  .rank(method='max')

vaccine_rank = utils.get_vaccination_per_country_rank(df_imf, selected_country)

# round the rank to the 2 decimals precision
vaccine_per_population = np.round(vaccine_per_population, decimals=2)

# calculate the total doses per hundred rank
df_vaccination_by_country['total_vaccination_per_hundred rank'] = \
    df_vaccination_by_country['total_vaccinations_per_hundred'].rank(method='max')

vaccination_rank = utils.get_total_vaccination_per_hundred_rank(df_vaccination_by_country, selected_country)

col1, col2 = st.columns([1,2])

with col1:

  st.title(f'{selected_country} ranking')

  secured_vaccine_html = f"""
  <p class="secured-vaccine"> secured vaccine: {vaccine_per_population} doses per person </p>
  <p class="rank">rank: {vaccine_rank}</p>
  <p class="vaccination-rate"> vaccination rate: {country_vaccination}% </p>
  <p class="rank"> rank: {vaccination_rank} </p>
  <p class="fully-vaccination-rate">fully vaccination rate: {country_fully_vaccination_rate}%</p>
  <p class="rank"> rank: {fully_vaccination_rank} </p>
  """
  st.markdown(secured_vaccine_html, unsafe_allow_html=True)

with col2:
  # merge the data from owid-covid-data to imf data
  st.title("Secured Vaccine (courses)")

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
        family="Roboto",
        size=18,
        color="#293fe3"
      )
    )
  secured_vaccine_data_chart\
    .update_traces(texttemplate='%{text:,}',marker_color='rgb(158,202,225)')

  st.plotly_chart(secured_vaccine_data_chart)
  
