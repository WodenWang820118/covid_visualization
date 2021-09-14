import streamlit as st
from multiapp import MultiApp
from apps import home, vaccination_time

app = MultiApp()

app.add_app("Home Page", home.app)
app.add_app("Vaccination rate comparison", vaccination_time.app)
app.run()