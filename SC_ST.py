import pandas as pd
import json
import plotly.express as px
import dash #(version 1.9.1) pip install dash==1.9.1
from dash import html
from dash import dash_table
import pandas as pd
from collections import OrderedDict
from dash.dash_table.Format import Group
from dash import dcc

import numpy as np
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("Final_CSVs\Crimes_Against_SC_ST_Test.csv")

candidates = df.columns[3:-1] 
years = df.YEAR.unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Crime:"),
    dcc.Dropdown(
        id='crime', 
        options=[{'value': x, 'label': x} 
                 for x in candidates],
        placeholder = "Choose a crime"
    ),
    html.P("Year:"),
    dcc.Dropdown(
        id='year', 
        options=[{'value': y, 'label': y} 
                 for y in years],
        placeholder = "Choose an Year"
    ),
    dcc.Graph(id="choropleth"),
])



@app.callback(
    Output("choropleth", "figure"), 
    [Input("crime", "value"), Input("year", "value")])
def display_choropleth(crime, year):
    finaldata = df.loc[df["YEAR"] == year]

    fig = px.choropleth(
        finaldata, geojson=json1, color=crime,
        locations="state_code", featureidkey="properties.state_code", hover_data=["AREA_NAME"])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

app.run_server()