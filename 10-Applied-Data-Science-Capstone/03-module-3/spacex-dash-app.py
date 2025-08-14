# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(["Launch Site: ", dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            )], style={'font-size': 20}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):", style={'font-size': 20}),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                               min=0, max=10000, step=1000,
                                               marks={0: '0',
                                                     2500: '2500',
                                                     5000: '5000',
                                                     7500: '7500',
                                                     10000: '10000'},
                                               value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Use all rows in the dataframe to render and return a pie chart graph to show the total success launches
        # Group by Launch Site and count successful launches
        fig = px.pie(spacex_df, values='class', 
                    names='Launch Site', 
                    title='Total Success Launches By Site')
        return fig
    else:
        # Filter the dataframe for the selected site
        # Render and return a pie chart graph to show the success (class=1) count and failed (class=0) count for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Create class labels for better visualization
        filtered_df['outcome'] = filtered_df['class'].map({0: 'Failure', 1: 'Success'})
        fig = px.pie(filtered_df, names='outcome', 
                    title=f"Total Success Launches for site {entered_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    # Filter data based on payload range
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                           (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        # Render a scatter plot to display all values for variable Payload Mass (kg) and variable class
        # Color-label the point using Booster Version Category
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                        color="Booster Version Category",
                        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # Filter the dataframe for the selected site and payload range
        # Render a scatter chart to show values Payload Mass (kg) and class for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                        color="Booster Version Category",
                        title=f"Correlation between Payload and Success for site {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run()