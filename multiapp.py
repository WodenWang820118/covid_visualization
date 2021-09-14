import streamlit as st

class MultiApp:
  """Framework for enabling the multi-page applications.
  """
  def __init__(self):
    self.apps = []
  
  def add_app(self, title, func):
    """Add a new application
    """
    self.apps.append({
      "title": title,
      "function": func,
    })
  
  def run(self):
    app = st.sidebar.radio(
      'Naviagtion',
      self.apps,
      format_func=lambda app: app['title']
    )
    app['function']()