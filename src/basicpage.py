from dash import Dash, html, dcc, no_update
from dash import Input, Output, callback, State, ctx
import dash_bootstrap_components as dbc

import analysis 
import plots 

from importlib import reload
reload(analysis)
reload(plots)

import os
import pandas as pd

# Set the path to the data files
PATH_CURRENCY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'clean_exchange_data.csv'))
PATH_CRISIS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'clean_crisis_data.csv'))

PATH_FAVICON = os.path.join('assets','favicon.ico')
PATH_ICON = os.path.join('assets', 'icon.png')
PATH_PAGE_DIV = os.path.join('assets', 'fancy_underline.png')

exchange_df = pd.read_csv(PATH_CURRENCY)
crisis_df = pd.read_csv(PATH_CRISIS)

def run_app() -> None:
    """
    Instantiate Dash app, giving it a title, icon, and layout, and then run the app.

    """
    # Create the application
    app = Dash(__name__, suppress_callback_exceptions=False)

    # The title will appear in the browser tab
    app.title = 'The Currency Capsule'

    # https://stackoverflow.com/questions/60023276/changing-the-favicon-in-flask-dash
    app._favicon = (PATH_FAVICON)

    # Create a layout
    create_layout(app)

    # This runs the app 
    app.run(debug=False)

    return None

def make_line_fig(price_country: str = "United States of America") -> plots.go.Figure:
    """
    Given a country, gather the years and the exchange rate data use that to create the figure.

    Arguments:
        price_country (str): the country selected, associated with the exchange rate line graph, defaulting
                             to the USA for a baseline.
    
    Output:
        fig (plots.go.Figure): the Plotly line graph figure object that will be displayed in the app. 
    """
    # Get the exchange rate data (x is the years, y is the exchange rates) for the selected country
    x, y = analysis.get_country_exchange_data(exchange_df, price_country)
    fig = plots.plotly_line(x, y)

    # Set margins
    fig.update_layout(margin=dict(t=3, b=30, l=30, r=30))

    return fig

def make_timeline_fig(crisis_country: str = "United States of America") -> plots.go.Figure:
    """
    Given a country, gather the years and the crisis data use that to create the figure.

    Arguments:
        crisis_country (str): the country selected, associated with the crisis scatter graph, defaulting
                              to the USA for a baseline.
    
    Output:
        fig (plots.go.Figure): the Plotly scatter graph figure object that will be displayed in the app. 
    """
    # Get the historical crisis/events dataframe for the selected country
    subset_crisis_df = analysis.get_country_crisis_data(crisis_df, crisis_country)

    # Hong Kong, Europe, and Israel have exchange rate data but not crisis data
    # Return an empty placeholder figure if no crisis data exists for the selected country
    if subset_crisis_df.empty:
        fig = plots.go.Figure()
        fig.update_layout(
            title_text=f"No crisis data available for {crisis_country}",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(24,34,37,0.7)',
            font=dict(color='#b59e5f'),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=600
        )
        return fig
    
    # Generate the scatter plot using the crisis data
    fig = plots.plotly_scatter(subset_crisis_df)
    fig.update_layout(margin=dict(t=3, b=30, l=30, r=30))

    return fig

# image credits:
# https://www.vecteezy.com/png/12634764-art-deco-outline-stroke-in-golden-color-for-classy-and-luxury-style-premium-vintage-line-art-design-element 
def create_layout(app: Dash) -> None:
    """
    Create the layout for the Dash app.

    Arguments:
        app (Dash): the app whose layout attribute will be this created layout.
    
    """
    # Get the list of countries and currencies from the exchange_df dataframe
    # and convert them to lists for the dropdown options
    country_list = exchange_df['country'].unique().tolist()
    currency_list = exchange_df['currency_name'].unique().tolist()

    # Create the layout for the app
    layout = html.Div(id='main-div',
                                # First div for the title and icon
                      children=[html.Div([html.H1('The Currency Capsule'),

                                          html.Img(src=PATH_ICON,
                                                   style={'height': '100px', 'marginRight': '20px'})
                                ],
                                style={'display': 'flex',
                                       'justifyContent': 'space-between',
                                       'alignItems': 'center',
                                       'flexDirection': 'row'}
                                ), 
                                # Second div for the description
                                html.H2('Your one-stop shop to understanding finances across time!'), 
                                
                                # Div for the input heading and informational popover to explain the inputs
                                html.Div([html.H3("Input:", style={"textDecoration": "underline"}),
                                          
                                          dbc.Button("?", id="component-target", n_clicks=0, className='popover-icon'),
                                          
                                          dbc.Popover([dbc.PopoverBody("Select a country, then a relevant currency, and lastly type in a year of choice, then press Estimate Exchange Rate!")],
                                                                        target="component-target",
                                                                        trigger="hover")
                                ], 
                                         style = {'display': 'flex', 
                                                  'flexDirection': 'row', 
                                                  'justifyContent': 'flex-start'}
                                ),

                                # Div for the inputs, place to input the country in a dropdown, 
                                # currency in a filtered dropdown, and year in a text area
                                # and the button to submit the values
                                # Also contains a button to reset the values
                                html.Div(id = "input_area", 
                                         children = [dcc.Dropdown(options = country_list, 
                                                                  id='select-country', 
                                                                  placeholder = 'Select a country..',
                                                                  style={'backgroundColor': '#182225',
                                                                         'color': '#b59e5f',
                                                                         'fontFamily': 'Unica One',
                                                                         'width': '300px', 
                                                                         'marginRight': '10px'}),

                                                    dcc.Dropdown(options = currency_list,
                                                                id='select-currency', 
                                                                placeholder = 'Select a currency..',
                                                                style={'backgroundColor': '#182225',
                                                                       'color': '#b59e5f',
                                                                       'width': '300px', 
                                                                       'fontFamily': 'Unica One',
                                                                       'marginRight': '10px'}),
                                        
                                                    dcc.Textarea(id='select-year',
                                                                 style={'width': '40px%', 
                                                                        'height':'35px',
                                                                        'paddingTop': '8px',
                                                                        'paddingLeft': '5px',
                                                                        'boxSizing': 'border-box',
                                                                        'fontFamily': 'Unica One', 
                                                                        'backgroundColor': '#182225',
                                                                        'color': '#FFFFFF'},
                                                                 placeholder = 'Enter a year...', 
                                                                 maxLength = 4, 
                                                                 minLength =4),

                                                    html.Button('Estimate Exchange Rate!', 
                                                                id='submit-val', 
                                                                n_clicks=0,
                                                                className='button_style'),

                                                    html.Button('Reset', 
                                                                id='reset-button',
                                                                n_clicks=0,
                                                                className='button_style')
                                          ], 
                                          style = {'display': 'flex', 
                                                   'flexDirection': 'row', 
                                                   'justifyContent': 'flex-start'}
                                ),
                                # Contains exchange rate output header, exchange rate output field, and a divider
                                # Also contains another informational popover to explain the exchange rates
                                html.H3(id='exchange-output', 
                                        children="Exchange Rate:", 
                                        style={"marginBottom":'25px', 
                                               'border':'1px solid #b59e5f', 
                                               "width": "fit-content", 
                                               'padding': '8px'}),
                                
                                html.Img(src=PATH_PAGE_DIV,
                                         style={'width': '400px', 
                                                'margin': '0 auto',
                                                'display': 'block'}),

                                html.Div([dbc.Button("?", 
                                                     id="note-nominal-er", 
                                                     n_clicks=0, 
                                                     className = "popover-icon"),

                                          dbc.Popover([dbc.PopoverBody("Note: the values shown here are nominal exchange rates, which means that inflation and consumer pricing index is not accounted for. The comparison to the USD in the exchange rate refers to the contemporaneous USD.")],
                                                                       target="note-nominal-er",
                                                                       trigger="hover")
                                ],
                                        style={'padding':'8px'}
                                ),
                                
                                # Div for the line graph and the timeline graph, side by side
                                # The line graph shows the country's exchange rate over time, 
                                # the timeline graph shows the country's historical crisis events
                                html.Div(id = "figure-area",
                                         children=[html.Div([html.H3(id = 'line-graph-title',
                                                                     children = ["Exchange Rate in United States of America's Currency Over Time", 
                                                                                 html.Br(),
                                                                                 "(Compared to the USD)"], 
                                                                     style={'textAlign': 'center'}),

                                                            dcc.Graph(id='line-figure', figure=make_line_fig()),
                                                    ], 
                                                    style={'flex': '1', 'display': 'inline-block', 'border': '1px solid #b59e5f'}
                                                    ),

                                                  html.Div([html.H3(id = 'timeline-title', 
                                                                    children = ["Timeline of Historical Events in United States of America"],
                                                                    style = {'textAlign':'center'}),

                                                            dcc.Graph(id='timeline-figure', figure= make_timeline_fig())
                                                  ], 
                                                            style={'flex': '1','display': 'inline-block', 'border': '1px solid #b59e5f'}
                                                  )   
                                         ], 
                                         style={'display': 'flex', 'flexDirection': 'row'}
                                ),

                                # Contains the image divider and another informational popover to explain the Euro
                                # and the countries that use it
                                html.Div([dbc.Button("?", 
                                                     id="note-euro", 
                                                     n_clicks=0, 
                                                     className = "popover-icon"),

                                          dbc.Popover([dbc.PopoverBody("Note: The European currency of the Euro was introduced January 1st, 1999. As of 2025, the countries Austria, Belgium, Croatia, Cyprus, Estonia, Finland, France, Germany, Greece, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, the Netherlands, Portugal, Slovakia, Slovenia and Spain use the Euro. The Currency Capsule includes the Euro as a currency under a separate country label of Europe.")],
                                                                       target="note-euro",
                                                                       trigger="hover")
                                ],
                                          style={'padding':'8px'}
                                ),
                                # Final divider
                                html.Img(src=PATH_PAGE_DIV,
                                         style={'width': '400px', 
                                                'margin': '0 auto',
                                                'display': 'block'}),
                                
                      ]
             )
    # Set the layout of the app to the created layout
    app.layout = layout

    return None

# Callback #1: currency dropdown filtering based on country selection
@callback(
    Output("select-currency", "options"),
    Input("select-country", "value")
)

def update_currency_options(selected_country: str) -> list:
    """
    The user selects a specific country from the select-country dropdown, so update the select-currency dropdown 
    accordingly so that only the currencies for that country are available to choose from. 

    Arguments:
        selected_country (str): the country selected by the user from the select-country dropdown.
    
    Output:
        options (list): the list of currency options to display and update the select-currency dropdown with. 
    """
    # No country selected, return empty list of options
    # This is the default state of the currency dropdown, which is empty
    if selected_country is None:
        return []
    
    # Filter the exchange_df dataframe to get the unique currency ranges for the selected country
    filtered = exchange_df[exchange_df['country'] == selected_country]
    unique_currency_ranges = filtered[['currency_name', 'currency_range']].drop_duplicates()
    
    # Create a list of dictionaries for the options in the dropdown
    options = []

    # Iterate through the unique currency ranges and create the options for the dropdown
    for idx, row in unique_currency_ranges.iterrows():
        options.append({"label": row['currency_range'], "value": row['currency_name']})

    return options

# Callback #2: exchange rate output, line graph, and timeline graph updates based on button clicks
# Merged two conflicting callbacks here with calback context as per:
# https://community.plotly.com/t/how-to-use-dash-callback-context-in-dynamic-callbacks/78447/3
@callback(
    Output('exchange-output', 'children'),
    Output('select-country', 'value'),
    Output('select-currency', 'value'),
    Output('select-year', 'value'),
    Output('line-figure', "figure"),
    Output('line-graph-title', 'children'),
    Output('timeline-figure', 'figure'),
    Output('timeline-title', 'children'),

    Input('submit-val', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    State('select-country', 'value'),
    State('select-currency', 'value'),
    State('select-year', 'value'),
    prevent_initial_call=True
)

def two_buttons(submit_val_clicks: int, 
                reset_clicks: int, 
                country: str, 
                currency: str, 
                year: str) -> list:
    """
    The user has selected one of the two buttons (reset-button or submit-val button), so the Dash must be updated 
    accordingly. 

    If the reset-button is selected, the exchange-output header value, the select-country dropdown value, the 
    select-currency dropdown value, the select-year text area value, the line-figure figure, the line-graph-title 
    header value, the timeline-figure figure, and the timeline-title header value must be reset to the USA default 
    or cleared altogether.

    If the submit-val button is selected, the exchange-output header value must be retrieved and displayed, and the 
    line-figure figure, the line-graph-title header value, the timeline-figure figure, and the timeline-title header 
    value must all be updated with the given inputs.

    Arguments:
        submit_val_clicks (int): the binary value (0 or 1) for if the submit-val button is selected.
        reset_clicks (int): the binary value (0 or 1) for if the reset-button button is selected.
        country (str): the country selected by the user from the select-country dropdown.
        currency (str): the currency selected by the user from the select-currency dropdown.
        year (str): the year inputed by the user from the select-year textbox.
    
    Output:
        (list): the list of 8 outputs to set the callback outputs to, consisting of the exchange-output header 
                value, the select-country dropdown value, the select-currency dropdown value, the select-year text 
                area value, the line-figure figure, the line-graph-title header value, the timeline-figure figure, 
                and the timeline-title header value.
    """
    # We need to know the context of which button(s) were clicked

    # No button clicked, return no update for all outputs (default)
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    # Button was clicked, get output and split it to get the button id
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # If user selected reset button, reset all 8 fields
    if triggered_id == 'reset-button':
        return "Exchange Rate:", None, None, "", make_line_fig(), "Currency Exchange in United States of America Over Time", make_timeline_fig(), "Timeline of Historical Events in United States of America"
    
    # If user selected submit button, update all 8 fields as needed
    if triggered_id == 'submit-val':
        
        # Check for incomplete fields, return missing data alert
        if not country or not currency or not year:
            return "Exchange rate: (missing data)", no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        # Initialize the figures
        updated_line_fig = make_line_fig(price_country=country)
        updated_timeline_fig = make_timeline_fig(crisis_country=country)

        # No incomplete fields, now check validity of query (exists?)
        try:
            rate = analysis.get_exchange_rate_val(exchange_df, country, currency, year)

            # Query doesn't exist as a possibility, return no data alert
            if rate == 0.0: 
                return (f"Exchange rate: no data for {country} and/or {currency} in {year}."), no_update, no_update, no_update, updated_line_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"], updated_timeline_fig, [f"Timeline of Historical Events in {country}"]

            # Query exists, now isolate the exchange rate
            return f"Exchange rate: {rate} {currency} per USD", no_update, no_update, no_update, updated_line_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"], updated_timeline_fig, [f"Timeline of Historical Events in {country}"]
        
        # Everything else failed, invalid input was likely given
        except Exception as e:
            return "Exchange rate: Please enter a valid four-digit year.", no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    # Just in case, return no update for all outputs (default)
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

