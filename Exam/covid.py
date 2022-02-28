from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

app = Dash(__name__)

data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
data = data.astype({'date':np.datetime64})
data['month'] = data['date'].dt.to_period('M').astype(str)
data['year'] = data['date'].dt.year
df = data.groupby(['year','month','continent','iso_code','location','life_expectancy','gdp_per_capita']).sum().reset_index()[['month','continent','location','gdp_per_capita','life_expectancy','new_cases']]
df['new_cases'] = df['new_cases'].mask(df['new_cases']<0,0)

app.layout = html.Div([
    html.Div([

        
        dcc.Dropdown(
            df['location'].unique(),
            'Vietnam',
            id='xaxis-column'
        ),
        # dcc.RadioItems(
        #     ['Linear', 'Log'],
        #     'Linear',
        #     id='xaxis-type',
        #     inline=True
        # )
        ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic')

    # dcc.Slider(
    #     df['month'][0],
    #     df['month'][len(df['month'])-1],
    #     step=None,
    #     id='month--slider',
    #     value=df['month'][len(df['month'])-1],
    #     marks={str(year): str(year) for year in df['month'].unique()},

    # )
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'))
    # Input('month--slider', 'value'))
def update_graph(year_value):
    dff = df[df['month'] == year_value]

    fig = px.scatter(df, x="gdp_per_capita", y="life_expectancy", animation_frame="month", 
                    animation_group="location", size="new_cases", color="continent", 
                    hover_name="location", log_x=True, size_max=55, 
                    range_x=[1000,100000], range_y=[60,90])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)