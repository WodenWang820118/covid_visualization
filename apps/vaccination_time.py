"""
The file is the page called vaccination rate comparition. It aims
for visualizing the vaccinated rate over time with the selected countries.
"""
import pandas as pd
import plotly.express as px
import streamlit as st
import utils

# pylint: disable=W0311

class Data:
  """Wrap the data in an object to pass the reference to the value
  """
  def __init__(self, data):
    self.df = pd.DataFrame(pd.read_csv(data))
    self.location_options = pd.unique(self.df['location'])
    self.choose_location = []
    self.choosen_location = []

  def choose_locations(self):
    """Return a multiselect tag box and a list of selected options
    """
    self.choose_location = st.multiselect('', self.location_options, 'Taiwan')
    return self.choose_location

  def get_choosen_locations(self):
    """Return the selected countries list data
    """
    for country in self.choose_location:
      self.choosen_location.append(country)
    return self.choosen_location

  def get_latest_date(self):
    """Return the latest day of the dataframe
    """
    return self.df['date'].max()

  def get_oldest_date(self):
    """Return the oldest day of the dataframe
    """
    return self.df['date'].min()

  def get_dataframe(self):
    """Return the dataframe of the instance
    """
    return self.df

def app():
  """The function is called by the app.py, as one of the pages of
  the application.
  """

  st.title("Vaccination rate over time")

  utils.local_css("style.css")

  df_obj = Data('data/vaccinations.csv')

  # get the time interval, using default daily frequencies
  new_idx = pd.date_range(
              start=df_obj.get_oldest_date(),
              end=df_obj.get_latest_date()) # for reindex, used use index

  # col1 for checkbox, col2 for data over time chart
  col1, col2 = st.columns([1,3])

  with col1:
    try:
      df_obj.choose_locations()
    except:
      st.write("Empty data or data doesn't exist.")

  with col2:
    try:
      selected_countries = df_obj.get_choosen_locations()
      vaccination_series = []

      for country in selected_countries:
        df = df_obj.get_dataframe()
        df_country = df.loc[df['location']==country]

        df_country.set_index(pd.to_datetime(df_country['date']), inplace=True)
        vaccination_rate = df_country[['total_vaccinations_per_hundred','location']]

        df_ = vaccination_rate.reindex(new_idx)
        upd_vaccination_rate = df_['total_vaccinations_per_hundred']

        # append series
        vaccination_series.append(upd_vaccination_rate)
        # zip selected countries and vaccination series into dictionary
        # convert to dataframe
        vaccination_data = dict(zip(selected_countries, vaccination_series))
        df_new = pd.DataFrame.from_dict(vaccination_data)

      fig = px.line(data_frame=df_new, x=df_new.index, y= df_new.columns)
      fig\
        .update_layout(
        yaxis_title=None,
        xaxis_title=None,
        autosize=True,
        margin=dict(l=0,r=0,t=0,b=0),
        width=1000, height=700,
        showlegend=True,
        legend=dict(
          title_text="Country"
        ),
        font=dict(
            family="Roboto",
            size=18,
            color="#293fe3"
          )
        )
      st.plotly_chart(fig)
    except:
      st.write("Empty option, or data doesn't exist.")
