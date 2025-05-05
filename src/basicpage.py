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
    app.run(debug=True)

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
    x, y = analysis.get_country_exchange_data(exchange_df, price_country)
    fig = plots.plotly_line(x, y)

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
    subset_crisis_df = analysis.get_country_crisis_data(crisis_df, crisis_country)

    # Hong Kong, Europe, and Israel have exchange rate data but not crisis data
    if subset_crisis_df.empty:
        # Return an empty placeholder figure if no crisis data
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
    country_list = exchange_df['country'].unique().tolist()
    currency_list = exchange_df['currency_name'].unique().tolist()

    layout = html.Div(id='main-div',
                      children=[html.Div([html.H1('The Currency Capsule'),

                                          html.Img(src=PATH_ICON,
                                                   style={'height': '100px', 'marginRight': '20px'})
                                ],
                                style={'display': 'flex',
                                       'justifyContent': 'space-between',
                                       'alignItems': 'center',
                                       'flexDirection': 'row'}
                                ), 
                                html.H2('Your one-stop shop to understanding finances across time!'), 
                                
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
                                
                                html.Img(src=PATH_PAGE_DIV,
                                         style={'width': '400px', 
                                                'margin': '0 auto',
                                                'display': 'block'}),
                                
                      ]
             )
    app.layout = layout

    return None

# currency dropdown filtering callback
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
    if selected_country is None:
        return []
    
    filtered = exchange_df[exchange_df['country'] == selected_country]
    unique_currency_ranges = filtered[['currency_name', 'currency_range']].drop_duplicates()
    
    options = []

    for idx, row in unique_currency_ranges.iterrows():
        options.append({"label": row['currency_range'], "value": row['currency_name']})

    return options


# merged two conflicting callbacks here with calback context as per:
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

    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # if user selected reset button, reset all 8 fields
    if triggered_id == 'reset-button':
        return "Exchange Rate:", None, None, "", make_line_fig(), "Currency Exchange in United States of America Over Time", make_timeline_fig(), "Timeline of Historical Events in United States of America"
    
    # if user selected submit button, update all 8 fields as needed
    if triggered_id == 'submit-val':
        
        # check for incomplete fields, return missing data alert
        if not country or not currency or not year:
            return "Exchange rate: (missing data)", no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        # initialize the figures
        updated_line_fig = make_line_fig(price_country=country)
        updated_timeline_fig = make_timeline_fig(crisis_country=country)

        # no incomplete fields, now check validity of query (exists?)
        try:
            rate = analysis.get_exchange_rate_val(exchange_df, country, currency, year)

            if rate == 0.0: # query doesn't exist as a possibility
                return (f"Exchange rate: no data for {country} and/or {currency} in {year}."), no_update, no_update, no_update, updated_line_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"], updated_timeline_fig, [f"Timeline of Historical Events in {country}"]

            # query exists, now isolate the exchange rate
            return f"Exchange rate: {rate} {currency} per USD", no_update, no_update, no_update, updated_line_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"], updated_timeline_fig, [f"Timeline of Historical Events in {country}"]
        
        
        except Exception as e:
            return "Exchange rate: Please enter a valid four-digit year.", no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

