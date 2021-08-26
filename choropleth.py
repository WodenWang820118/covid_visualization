import streamlit as st
import pandas as pd
import plotly.express as px

vaccination_data = pd.read_csv(r'D:\Master of IT\Semester4\Information visualization\assignment2\streamlit\dataset\covid-19-vaccination-rate-by-country/vaccinations.csv')
df = pd.DataFrame(vaccination_data)

def vaccination_lastest_date_by_country(df):
  return df.groupby('location').last().reset_index()

country_lastest_vaccination = vaccination_lastest_date_by_country(df)

df_vaccination_by_country = country_lastest_vaccination.sort_values(by='total_vaccinations_per_hundred', ascending=True)

fig_map = px.choropleth(df_vaccination_by_country, locations="iso_code",
                    color="total_vaccinations_per_hundred", 
                    hover_name="location",
                    color_continuous_scale=px.colors.sequential.Plasma) # should be able to adjust the color

fig_map.update_layout(autosize=False, width= 1200, height=800)

st.set_page_config(layout="wide")
st.plotly_chart(fig_map)