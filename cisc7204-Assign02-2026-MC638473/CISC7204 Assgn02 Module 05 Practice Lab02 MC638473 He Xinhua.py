import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt

DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
)

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

df = pd.read_csv(DATA_URL)

df["Month"] = pd.to_datetime(df["Date"]).dt.month_name()
df["Year"] = pd.to_datetime(df["Date"]).dt.year

REGION_OPTIONS = [
    {"label": "New South Wales", "value": "NSW"},
    {"label": "Northern Territory", "value": "NT"},
    {"label": "Queensland", "value": "QL"},
    {"label": "South Australia", "value": "SA"},
    {"label": "Tasmania", "value": "TA"},
    {"label": "Victoria", "value": "VI"},
    {"label": "Western Australia", "value": "WA"},
]
YEAR_OPTIONS = [
    {"label": str(y), "value": int(y)} for y in sorted(df["Year"].unique())
]

app.layout = html.Div(
    children=[
        html.H1(
            "Australia Wildfire Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 26},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Select Region:", style={"margin-right": "2em"}),
                        dcc.RadioItems(
                            options=REGION_OPTIONS,
                            value="NSW",
                            id="region",
                            labelStyle={"display": "inline-block", "margin-right": "1em"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H2("Select Year:", style={"margin-right": "2em"}),
                        dcc.Dropdown(options=YEAR_OPTIONS, value=2005, id="year"),
                    ]
                ),
                html.Div(
                    [
                        html.Div([], id="plot1"),
                        html.Div([], id="plot2"),
                    ],
                    style={"display": "flex"},
                ),
            ]
        ),
    ]
)


@app.callback(
    [
        Output(component_id="plot1", component_property="children"),
        Output(component_id="plot2", component_property="children"),
    ],
    [
        Input(component_id="region", component_property="value"),
        Input(component_id="year", component_property="value"),
    ],
)
def reg_year_display(input_region, input_year):
    region_data = df[df["Region"] == input_region]
    y_r_data = region_data[region_data["Year"] == input_year]

    est_data = y_r_data.groupby("Month")["Estimated_fire_area"].mean().reset_index()
    fig1 = px.pie(
        est_data,
        values="Estimated_fire_area",
        names="Month",
        title="{} : Monthly Average Estimated Fire Area in year {}".format(
            input_region, input_year
        ),
    )

    veg_data = y_r_data.groupby("Month")["Count"].mean().reset_index()
    fig2 = px.bar(
        veg_data,
        x="Month",
        y="Count",
        title="{} : Average Count of Pixels for Presumed Vegetation Fires in year {}".format(
            input_region, input_year
        ),
    )

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


if __name__ == "__main__":
    app.run_server(debug=False)
