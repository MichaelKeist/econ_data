import requests
from urllib.request import urlopen
import json
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def make_plot(df, variable, range_min, range_max, legend_name):
    fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df["fips"], z=df[variable],
                           marker_line_width=0,
                           colorscale="Viridis",
                           zmin = range_min,
                           zmax = range_max,))
    fig.update_layout(mapbox_style = "light", mapbox_accesstoken = token, mapbox_zoom=2.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, text = "test")
    fig.update_layout(margin={"r":0,"t":1,"l":0,"b":0})
    fig.write_image("/home/michael/fun_projects/data_science/trial.jpg")


token = "pk.eyJ1IjoibXdrZWlzdCIsImEiOiJja3l4Z2Q0cXcwaHFlMm9xcGJ6NHBsNjRyIn0.gIb7UDMbMMbRthoYZ9ubjQ"
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
	counties = json.load(response)
#raw_data = requests.get("https://apps.bea.gov/api/data/?&UserID=8F132E0E-C07F-4FC8-8A8D-28DE870B6E0C&DatasetName=Regional&GeoFips=COUNTY&TableName=CAEMP25N&LineCode=10&Method=GetData")
#data_dict = raw_data.json()["BEAAPI"]["Results"]
#
#w = open("/home/michael/fun_projects/data_science/sample_data.csv", "wb")
#pickle.dump(data_dict, w)
#w.close()

w = open("/home/michael/fun_projects/data_science/jobs_data.csv", "rb")
data_dict = pickle.load(w)
w.close()
data_dict = data_dict["Data"]

county_list = []
data_list = []
date_list = []
na_list = []
count = 0
for item in data_dict:
    if item["TimePeriod"] == "2020":
        if item["DataValue"] != "(NA)":
            date_list.append(int(item["TimePeriod"]))
            county_list.append(int(item["GeoFips"]))
            data_list.append(int(item["DataValue"].replace(",", "")))
        else:
            na_list.append(item["GeoFips"])

dict_input = {"fips": county_list, "jobs": data_list}
data_frame = pd.DataFrame(dict_input)

make_plot(data_frame, "jobs", 0, 120000, "Total Jobs")
