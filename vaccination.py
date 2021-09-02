'''
    filename: vaccination.py
    Author: Chien-Chih Wang
    description:
    The file contains two parts. One is the bar chart with top 20 coutries that
    has the highest vaccination doses per hundread, denoted as 'total_vaccinations_per_hundred'.
    Another part is the choropleth map with vaccination.
'''
import os
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# TODO: fix the path specified to deploy and local use -> should take out the vaccination.py; remain the path of data; change the run in Procfile
current_directory = os.getcwd()
print(current_directory)
# set the page configuration at the beginning, then renders the content
st.set_page_config(layout="wide")

# data
def vaccination_lastest_date_by_country(dataframe):
  '''group the data by location and get last date data'''
  return dataframe.groupby('location').last().reset_index()

vaccination_data = pd.read_csv('vaccinations.csv')
df = pd.DataFrame(vaccination_data)

imf_data = pd.read_csv('imf-who-covid-19-vaccine-supply-tracker.csv',skiprows=2, engine='python')
df_imf = pd.DataFrame(imf_data)

country_lastest_vaccination = vaccination_lastest_date_by_country(df)
df_vaccination_by_country = country_lastest_vaccination\
                            .sort_values(by='total_vaccinations_per_hundred', ascending=True)

# title, input, layout
# TODO: title is confusing
st.title("COVID-19 vaccine doses administered per 100 people")
# st.markdown("<h1 style='text-align: center;'>Vaccination Rate by Country</h1>",
#             unsafe_allow_html=True)

############################ choropleth map section ############################
# TODO: colors to 4-5 classes
# reference: https://waynestalk.com/en/python-choropleth-map-en/
def group_vaccination(x):
  if x < 40:
    return f'{0}~{40}'
  elif x < 80:
    return f'{40}~{80}'
  elif x < 120:
    return f'{80}~{100}'
  elif x < 160:
    return f'{120}~{160}'
  elif x < 200:
    return f'{160}~{200}'
  else:
    return f'{200} above'
# TODO: highlight the country selected
df_vaccination_by_country['doses administered per 100 people'] = df_vaccination_by_country\
                                ['total_vaccinations_per_hundred'].apply(group_vaccination)

custom_data = df_vaccination_by_country['location'].tolist()

colors = ['#edf8e9','#c7e9c0','#bae4b3','#74c476','#31a354','#006d2c']
fig_map = px.choropleth\
                    (df_vaccination_by_country,
                    locations="iso_code",
                    color="doses administered per 100 people",
                    hover_name="location",
                    color_discrete_sequence=colors,)

fig_map.update_layout(autosize=False, width= 1200, height=800)
st.plotly_chart(fig_map)
############################ sidebar section ############################

countries = df_vaccination_by_country.sort_values(by='location')['location'].tolist()

selected_country = st.sidebar.selectbox('Select a country', countries, index=countries.index('Taiwan'))

country_vaccination = df_vaccination_by_country[df_vaccination_by_country['location']==selected_country]\
                                                ['total_vaccinations_per_hundred'].values[0]

st.sidebar.text(f"{selected_country} vaccination rate is: {country_vaccination}%")
vaccination_avg = df_vaccination_by_country['total_vaccinations_per_hundred'].mean().round(decimals=2)
  
st.sidebar.text(f"The world average: {vaccination_avg}%")


############################ bar chart section ############################
df_imf = df_imf.rename(columns={"ISO3":"iso_code"})

df_country = df_vaccination_by_country[['location','iso_code']]
df_imf = df_imf.merge(df_country, on='iso_code', how='inner')

total_vaccinations = df_vaccination_by_country[df_vaccination_by_country['location']==selected_country]['total_vaccinations']
people_vaccinated = df_vaccination_by_country[df_vaccination_by_country['location']==selected_country]['people_vaccinated']
people_fully_vaccinated = df_vaccination_by_country[df_vaccination_by_country['location']==selected_country]['people_fully_vaccinated']
population = df_imf[df_imf['location']==selected_country]['Population']

# not_vaccinated_or_one = population - people_fully_vaccinated
data = [total_vaccinations, people_vaccinated,people_fully_vaccinated, population]

individual_data = px.bar(
  data,
  orientation='h',
  text=data)

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

components.html(
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
)

st.title("Secured Vaccine (courses)")
df_imf = df_imf.rename(columns={"Secured Vaccine (millions of courses)": "Secured Vaccine (courses)"}) # rename to fit the label
secured_vaccine = df_imf[df_imf['location']==selected_country]['Secured Vaccine (courses)'].apply(lambda x:x*1000000) # times 1 million to calcualte the ratio
secured_vaccine_data = [population, secured_vaccine]

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
secured_vaccine_data_chart.update_traces(texttemplate='%{text:,}',marker_color='rgb(158,202,225)')
st.plotly_chart(secured_vaccine_data_chart)

# TODO: the analysis on the chart; how to read
# TODO: any improvement?