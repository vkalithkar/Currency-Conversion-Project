# Dash: The application class
# html: Various HTML components
# dcc: Dash core components (things like buttons, figures, slider bars, etc.)
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
exchange_df = pd.read_csv(PATH_CURRENCY)
country_to_currency, currency_to_country  = analysis.get_countrycurrency_dicts(exchange_df)

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
    # app.run(debug=False)

    return None

def make_line_fig(price_country: str = "Argentina") -> plots.go.Figure:
    x, y = analysis.get_country_data(exchange_df, price_country)
    fig = plots.plotly_line(x, y)

    fig.update_layout(margin=dict(t=3, b=30, l=30, r=30))
    return fig

def make_timeline_fig() -> plots.go.Figure:
    fig = plots.plotly_timeline()
    fig.update_layout(margin=dict(t=3, b=30, l=30, r=30))
    return fig

def create_layout( app: Dash, exchange_df: pd.DataFrame) -> None:
    country_list = exchange_df['country'].unique().tolist()
    currency_list = exchange_df['currency_name'].unique().tolist()

    layout = html.Div(id='main-div',
                      children=[html.H1('The Currency Capsule'),  # This is a large header
                                html.H2('Your one-stop shop to understanding finances across time!'), # This is a smaller header

                                html.H3("Input:"),
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
                                                   'justifyContent': 'flex-start', 
                                                   'padding': '10px'}),
                                html.H3(id='exchange-output', children="Exchange Rate:"),
                                html.Small("Note: Europe"),
                                html.Div(id = "figure-area",
                                         children=[
                                            html.Div([
                                                html.H3(id = 'line-graph-title',
                                                        children = ["Exchange Rate in Argentina's Currency Over Time", 
                                                                    html.Br(),
                                                                    "(Compared to the USD)"], 
                                                        style={'textAlign': 'center'}),
                                                dcc.Graph(id='my-line-figure', figure=make_line_fig())
                                            ], 
                                            style={'flex': '1', 'display': 'inline-block', 'border': '1px solid #b59e5f'}),

                                            html.Div([
                                                html.H3("Timeline of Historical Events",
                                                        style = {'textAlign':'center'}),
                                                dcc.Graph(id='time-figure', figure=make_timeline_fig())
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
    options = [{"label": curr, "value": curr} for curr in country_to_currency.get(selected_country, [])]
    return options

# merged two conflicting callbacks here with calback context as per:
# https://community.plotly.com/t/how-to-use-dash-callback-context-in-dynamic-callbacks/78447/3
@callback(
    Output('exchange-output', 'children'),
    Output('select-country', 'value'),
    Output('select-currency', 'value'),
    Output('select-year', 'value'),
    Output('my-line-figure', "figure"),
    Output('line-graph-title', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    State('select-country', 'value'),
    State('select-currency', 'value'),
    State('select-year', 'value'),
    prevent_initial_call=True
)
def two_buttons(submit_val_clicks, reset_clicks, country, currency, year):
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == 'reset-button':
        return "Exchange Rate:", None, None, "", make_line_fig(), "Currency Exchange in Country Over Time"
    
    if triggered_id == 'submit-val':
        updated_fig = make_line_fig(price_country=country)
        if not country or not currency or not year:
            return "Exchange rate: (missing data)", no_update, no_update, no_update, no_update, no_update
        try:
            year = int(year)
            subset = exchange_df[
                (exchange_df['country'] == country) &
                (exchange_df['currency_name'] == currency) &
                (exchange_df['year'] == year)
            ]
            if subset.empty:
                return f"Exchange rate: no data for {country} and/or {currency} in {year}.", no_update, no_update, no_update, updated_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"]
            rate = subset.iloc[0]['exchange_rate']
            return f"Exchange rate: {rate} {currency} per USD", no_update, no_update, no_update, updated_fig, [f"Exchange Rate in {country}'s Currency Over Time", html.Br(), f"(Compared to the USD)"]
        except Exception as e:
            return f"Exchange rate: error - {str(e)}", no_update, no_update, no_update, no_update, no_update
    
    return no_update, no_update, no_update, no_update, no_update, no_update
