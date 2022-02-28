import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
data = data.astype({'date':np.datetime64})
data['month'] = data['date'].dt.to_period('M').astype(str)
data['year'] = data['date'].dt.year
df = data.groupby(['year','month','continent','iso_code','location','life_expectancy','gdp_per_capita']).sum().reset_index()[['month','continent','location','gdp_per_capita','life_expectancy','new_cases']]
df['new_cases'] = df['new_cases'].mask(df['new_cases']<0,0)
animations = {
    'Scatter': px.scatter(
        df, x="gdp_per_capita", y="life_expectancy", animation_frame="month", 
        animation_group="location", size="new_cases", color="continent", 
        hover_name="location", log_x=True, size_max=55, 
        range_x=[1000,100000], range_y=[60,90]),
    'Bar': px.bar(
        df, x="continent", y="new_cases", color="continent", 
        animation_frame="month", animation_group="location", 
        range_y=[0,1000000]),
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Select an animation:"),
    dcc.RadioItems(
        id='selection',
        options=[{'label': x, 'value': x} for x in animations],
        value='Scatter'
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    [Input("selection", "value")])
def display_animated_graph(s):
    return animations[s]

app.run_server(debug=True)