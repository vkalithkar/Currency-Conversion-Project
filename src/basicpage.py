from dash import Dash, html, dcc, no_update
from dash import Input, Output, callback, State, ctx

import analysis 
import plots 

from importlib import reload
reload(analysis)
reload(plots)

import os
import pandas as pd

# PATH_CURRENCY = os.path.join('..', 'data', 'clean_exchange_data.csv')
PATH_CURRENCY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'clean_exchange_data.csv'))
PATH_CRISIS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'clean_crisis_data.csv'))

exchange_df = pd.read_csv(PATH_CURRENCY)
crisis_df = pd.read_csv(PATH_CRISIS)

def run_app() -> None:
    # Create the application
    app = Dash(__name__, suppress_callback_exceptions=True)

    # The title will appear in the browser tab
    app.title = 'The Currency Capsule'

    # Create a layout
    create_layout(app, exchange_df)

    # This runs the app. 
    # Only include debug=True when testing, it shows an additional menu on the webpage
    app.run(debug=True)

    return None

def make_line_fig(price_country: str = "United States of America") -> plots.go.Figure:
    x, y = analysis.get_country_exchange_data(exchange_df, price_country)
    fig = plots.plotly_line(x, y)

    fig.update_layout(margin=dict(t=3, b=30, l=30, r=30))
    return fig

def make_timeline_fig(crisis_country: str = "United States of America") -> plots.go.Figure:
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

def create_layout(app: Dash, exchange_df: pd.DataFrame) -> None:
    country_list = exchange_df['country'].unique().tolist()
    currency_list = exchange_df['currency_name'].unique().tolist()

    layout = html.Div(id='main-div',
                      children=[html.H1('The Currency Capsule'),  # This is a large header
                                html.H2('Your one-stop shop to understanding finances across time!'), # This is a smaller header

                                html.H3("Input:", style={"textDecoration": "underline"}),
                                html.Div(id = "input_area", 
                                         children = [
                                            dcc.Dropdown(options = country_list, 
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

                                            html.Button('Estimate Exchange Rate!', id='submit-val', n_clicks=0,
                                                        className='button_style'),

                                            html.Button('Reset', id='reset-button', n_clicks=0,
                                                        className='button_style')
                                          ], 
                                          style = {'display': 'flex', 
                                                   'flexDirection': 'row', 
                                                   'justifyContent': 'flex-start' 
                                                   }),
                                html.H3(id='exchange-output', children="Exchange Rate:", style={"marginBottom":'25px', 'border':'1px solid #b59e5f', "width": "fit-content", 'padding': '8px'}),
                                html.Small(id='note-nominal-er', 
                                           children = "Note: the values shown here are nominal exchange rates, which means that inflation and consumer pricing index is not accounted for. The comparison to the USD in the exchange rate refers to the contemporaneous USD.",
                                          ),
                                html.Div(id = "figure-area",
                                         children=[
                                            html.Div([
                                                html.H3(id = 'line-graph-title',
                                                        children = ["Exchange Rate in United States of America's Currency Over Time", 
                                                                    html.Br(),
                                                                    "(Compared to the USD)"], 
                                                        style={'textAlign': 'center'}),
                                                dcc.Graph(id='line-figure', figure=make_line_fig()),
                                                html.Small(id='note-euro', 
                                                           children = "Note: The European currency of the Euro was introduced January 1st, 1999. As of 2025, the countries Austria, Belgium, Croatia, Cyprus, Estonia, Finland, France, Germany, Greece, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, the Netherlands, Portugal, Slovakia, Slovenia and Spain use the Euro. The Currency Capsule includes the Euro as a currency under a separate country label of Europe.",
                                                           )
                                            ], 
                                            style={'flex': '1', 'display': 'inline-block', 'border': '1px solid #b59e5f'}),

                                            html.Div([
                                                html.H3(id = 'timeline-title', 
                                                        children = ["Timeline of Historical Events in United States of America"],
                                                        style = {'textAlign':'center'}),
                                                dcc.Graph(id='timeline-figure', figure= make_timeline_fig())
                                            ], 
                                            style={'flex': '1','display': 'inline-block', 'border': '1px solid #b59e5f',})
                                         ], 
                                    style={'display': 'flex', 'flexDirection': 'row'}
                                )
                        ]
            )
    app.layout = layout
    return None

# dropdown filtering callback
@callback(
    Output("select-currency", "options"),
    Input("select-country", "value")
)
def update_currency_options(selected_country):
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
def two_buttons(submit_val_clicks, reset_clicks, country, currency, year):
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # if user selected reset button, reset all 8 fields
    if triggered_id == 'reset-button':
        return "Exchange Rate:", None, None, "", make_line_fig(), "Currency Exchange in United States of America Over Time", make_timeline_fig(), "Timeline of Historical Events in United States of America"
    
    # if user selected submit button, update all 8 fields as needed
    if triggered_id == 'submit-val':
        # initialize the figures
        updated_line_fig = make_line_fig(price_country=country)
        updated_timeline_fig = make_timeline_fig(crisis_country=country)

        # check for incomplete fields, return missing data alert
        if not country or not currency or not year:
            return "Exchange rate: (missing data)", no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        # no incomplete fields, now check validity of query (exists?)
        try:
            subset = analysis.get_exchange_subset(exchange_df, country, currency, year)

            if subset.empty: # query doesn't exist as a possibility
                return (f"Exchange rate: no data for {country} and/or {currency} in {year}."), no_update, no_update, no_update, updated_line_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"], updated_timeline_fig, [f"Timeline of Historical Events in {country}"]
            
            # query exists, now isolate the exchange rate
            rate = subset.iloc[0]['exchange_rate']
            return f"Exchange rate: {rate} {currency} per USD", no_update, no_update, no_update, updated_line_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"], updated_timeline_fig, [f"Timeline of Historical Events in {country}"]
        
        
        except Exception as e:
            return f"Exchange rate: error - {str(e)}", no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

