"""
The file contains:
  1. The name of the data set with data source link.
  2. The explicit data frames from the data set.
The page aims for the user to explore the data set itself.
"""

import pandas as pd
import streamlit as st
from core import utils

# TODO: write some contents in the page to explain the table
# TODO: bring the data source link to this page

def app():
  utils.local_css("style.css")

  st.title("Data Source")
  
  # data source: https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations
  vaccination_data = pd.read_csv('data/vaccinations.csv')
  df = pd.DataFrame(vaccination_data)
  
  vaccination_html=f"""
  <a href="https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations">
    <h2 class="link">Vaccinations</h2>
  </a>
  """
  st.markdown(vaccination_html, unsafe_allow_html=True)

  st.dataframe(df, height=700)

  vaccination_explain=f"""
  <p>The data set tracks the vaccinations in with various methods based on time and countries</p>
  """
  st.markdown(vaccination_explain, unsafe_allow_html=True)

  # imf vaccine secured data
  # data source: https://www.imf.org/en/Topics/imf-and-covid19/IMF-WHO-COVID-19-Vaccine-Supply-Tracker
  imf_data = pd.read_csv('data/imf-who-covid-19-vaccine-supply-tracker.csv',
                          skiprows=2, engine='python')
  df_imf = pd.DataFrame(imf_data)
  vaccine_secured_html=f"""
  <a href="https://www.imf.org/en/Topics/imf-and-covid19/IMF-WHO-COVID-19-Vaccine-Supply-Tracker">
    <h2 class="link">IMF WHO COVID-19 Vaccine Supply Tracker</h2>
  </a>
  """
  st.markdown(vaccine_secured_html, unsafe_allow_html=True)

  st.dataframe(df_imf, height=700)
  
  secured_vaccine_html=f"""
  <p>The data set tracks the number of vaccines secured by countries</p>
  """
  st.markdown(secured_vaccine_html, unsafe_allow_html=True)