import streamlit as st
from core.multiapp import MultiApp
from apps import home, vaccination_time, data

app = MultiApp()
app.add_app("Home Page", home.app)
app.add_app("Vaccination rate comparison", vaccination_time.app)
app.add_app("Data Source", data.app)
app.run()