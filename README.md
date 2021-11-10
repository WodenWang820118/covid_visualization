# Why are there many folders and files?
The folder stores the information needed for testing, data processing.
Below is the overview of the folders.
  - `__pycache__`: Python caches the compiled version of each module.
  - `.vscode`: the setting json of the editor.
  - `apps`: **the content of the application**
  - `core`: **the helper classes, and functions**
  - `data`: the CSV, xlsx data source files.
  - `jupyter`: the jupyter notebook for data processing testing.
  - `others`: the notes during the development.

# Where are the contents?
The contents are mainly in the `apps` folder with Python files.
The reason using Python to build a website is that it gives the flexibility
to pre-process and extract the necessary data. Although JavaScript also
provides similar libraries, under the time constraint, Python Pandas, Plotly
are comfortable to use.

# What is streamlit? Is it good for the data visualization?
The streamlit is a Python library, providing the interface for bringing
the charts, maps into a website without manipulating the DOM. The feature
hugely reduces the learning curve of the website building, but remains
the power of showcasing the data visualization, explorations and insights.

# What are other files for apart from index.html, style.css?
  - `app.py`: the file for activating the application.
  - `setup.sh`, `Procfile`, `requirements.txt`: for website deployment.









