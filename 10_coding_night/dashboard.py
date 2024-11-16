import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import wbdata
import pandas as pd
import plotly.express as px
import webbrowser
import threading

# Load the data
# Define the indicator for population (SP.POP.TOTL)
indicator = {
    'SP.POP.TOTL': 'total_population',  # Population 
    'SM.POP.NETM': 'net_migration'     # Net Migration
}
# Define countries (India, Pakistan, Bangladesh, Sri Lanka, Afghanistan)
# countries = ['IN', 'PK', 'BD', 'LK', 'AF']  # ISO codes
# Fetch data
data = wbdata.get_dataframe(indicator, 
                            # country=countries
                            )
# Reset index to convert it into a DataFrame
data.reset_index(inplace=True)
# Rename columns for clarity
data.rename(columns={'country': 'Country', 'date': 'Year'}, inplace=True)
# Ensure Year column is numeric
data['Year'] = pd.to_numeric(data['Year'])
# Filter data between 1960 and 2023
data = data[(data['Year'] >= 1960) & (data['Year'] <= 2023)]

# Create a DataFrame
df = data.copy()

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Migration and Population Dashboard Developed by Codanics", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Countries:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Country'].unique()],
            value=['Pakistan'],  # Default value
            multi=True,  # Enable multiple selection
            style={'width': '70%'}
        ),
    ]),
    html.Div([
        html.Label("Select Year Range:"),
        dcc.RangeSlider(
            id='year-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            step=1,
            value=[2010, 2023],  # Default range
            marks={year: str(year) for year in range(df['Year'].min(), df['Year'].max() + 1, 5)}
        )
    ], style={'margin-top': '20px'}),
    html.Div([
        dcc.Graph(id='line-plot'),
        dcc.Graph(id='line-plot1'),
        dcc.Graph(id='scatter-plot'),
    ])
])

# Callback to update plots based on selected countries and year range
@app.callback(
    [Output('line-plot', 'figure'), Output('line-plot1', 'figure'), Output('scatter-plot', 'figure')],
    [Input('country-dropdown', 'value'), Input('year-slider', 'value')]
)
def update_plots(selected_countries, selected_years):
    # Filter data for the selected countries and year range
    filtered_df = df[df['Country'].isin(selected_countries)]
    filtered_df = filtered_df[(filtered_df['Year'] >= selected_years[0]) & (filtered_df['Year'] <= selected_years[1])]

    # Line plot for total population over years
    line_fig = px.line(
        filtered_df,
        x='Year',
        y='total_population',
        color='Country',
        title=f'Total Population Over Years for {", ".join(selected_countries)}',
        labels={'total_population': 'Total Population', 'Year': 'Year'}
    )

    # Line plot for net migration over years
    line_fig1 = px.line(
        filtered_df,
        x='Year',
        y='net_migration',
        color='Country',
        title=f'Net Migration Over Years for {", ".join(selected_countries)}',
        labels={'net_migration': 'Net Migration', 'Year': 'Year'}
    )

    # Scatter plot for net migration vs. total population
    scatter_fig = px.scatter(
        filtered_df,
        x='net_migration',
        y='total_population',
        color='Country',
        title=f'Net Migration vs. Total Population for {", ".join(selected_countries)}',
        labels={'net_migration': 'Net Migration', 'total_population': 'Total Population'},
        size='total_population',  # Optional: size of markers
    )

    return line_fig, line_fig1, scatter_fig

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")


# Run the app
if __name__ == '__main__':
     # Start the browser in a separate thread
    threading.Timer(1, open_browser).start()
    app.run_server(debug=True)
