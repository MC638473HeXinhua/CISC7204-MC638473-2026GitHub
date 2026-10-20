import pandas as pd
import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding="ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Total number of flights to the destination state split by reporting airline',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    html.Div(["Input Year: ", dcc.Input(id='input-year', value='1998', 
                                        type='number', style={'height': '50px', 'font-size': 35})],
             style={'font-size': 40}),
    
    html.Br(),
    html.Br(),
    
    html.Div(dcc.Graph(id='bar-plot')),
])

@app.callback(Output(component_id='bar-plot', component_property='figure'),
              Input(component_id='input-year', component_property='value'))

def get_graph(entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    
    bar_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    
    fig = px.bar(bar_data, x='DestState', y='Flights', title='Flights to Destination State')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)