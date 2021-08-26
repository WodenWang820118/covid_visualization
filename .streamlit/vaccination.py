'''
    filename: vaccination.py
    Author: Chien-Chih Wang
    description:
    The file contains two parts. One is the bar chart with top 20 coutries that
    has the highest vaccination doses per hundread, denoted as 'total_vaccinations_per_hundred'.
    Another part is the choropleth map with vaccination.
'''

import pandas as pd
import plotly.express as px
import streamlit as st

# set the page configuration at the beginning, then renders the content
st.set_page_config(layout="wide")

# data
def vaccination_lastest_date_by_country(dataframe):
  '''group the data by location and get last date data'''
  return dataframe.groupby('location').last().reset_index()

vaccination_data = pd.read_csv('.streamlit/vaccinations.csv')
df = pd.DataFrame(vaccination_data)

country_lastest_vaccination = vaccination_lastest_date_by_country(df)
df_vaccination_by_country = country_lastest_vaccination\
                            .sort_values(by='total_vaccinations_per_hundred', ascending=True)

# title, input, layout
st.markdown("<h1 style='text-align: center;'>Top 20 vaccination countries</h1>",
            unsafe_allow_html=True)

############################ sidebar section ############################
st.sidebar.title("Search")
user_input = st.sidebar.text_input("The country you want to know: ", "Taiwan")
country_vaccination = df_vaccination_by_country[df_vaccination_by_country['location']==user_input]\
                                                ['total_vaccinations_per_hundred'].values[0]
st.sidebar.text(f"The {user_input} vaccination rate is: {country_vaccination}")
vaccination_avg = df_vaccination_by_country['total_vaccinations_per_hundred'].mean()
st.sidebar.text(f"The world average is: {vaccination_avg}")

############################ bar chart section ############################
fig = px.bar(df_vaccination_by_country[:20],
            x='total_vaccinations_per_hundred',
            y='location',
            text='total_vaccinations_per_hundred')
# prvent labels from overlapping
fig.update_yaxes(automargin=True)
fig.update_xaxes(automargin=True)

# bring the label text outside of the bar, and make the text bigger
# reference: https://plotly.com/python/bar-charts/#bar-chart-with-direct-labels
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# adjusting the axis labels and layout
fig.update_layout(yaxis_title=None, xaxis={"side": "top"}, autosize=False, width= 1200, height=500)

############################ choropleth map section ############################
fig_map = px.choropleth\
                    (df_vaccination_by_country,
                    locations="iso_code",
                    color="total_vaccinations_per_hundred",
                    hover_name="location",
                    # should be able to adjust the color
                    color_continuous_scale=px.colors.sequential.Plasma)

fig_map.update_layout(autosize=False, width= 1200, height=800)

############################ plotting figures on streamlit ############################
st.plotly_chart(fig)
st.plotly_chart(fig_map)
