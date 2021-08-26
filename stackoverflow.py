import plotly.express as px
import pandas as pd
import io
import requests
from IPython.core.display import display, HTML

# get and prepare data...
# df = pd.read_csv(io.StringIO(
#     requests.get("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv").text))
vaccination_data = pd.read_csv('owid-covid-data.csv')
df = pd.DataFrame(vaccination_data)

df["date"] = pd.to_datetime(df["date"])
dfp = df.dropna(subset=["continent", "total_vaccinations_per_hundred"]).loc[
    :, ["iso_code", "location", "date", "total_vaccinations_per_hundred"]
].sort_values("date").groupby("iso_code").last()


# give 15 pixels to each country for height
buffer = io.StringIO()
px.bar(dfp.sort_values("location", ascending=False),
       x="total_vaccinations_per_hundred",
       y="location",
       orientation="h"
      ).update_layout(height=len(dfp)*15).write_html(buffer, full_html=False)


# use HTML techniques for scoll bar, set heigh as required
HTML('<div style="overflow-y:scroll;height: 200px;">' + buffer.getvalue().encode().decode() + "</div>")
