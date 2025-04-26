from dash import Dash, html, dcc, Input, Output
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import dash_bootstrap_components as dbc
import os

# Load your clean_crisis_data.csv
PATH_CRISIS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'clean_crisis_data.csv'))
crisis_df = pd.read_csv(PATH_CRISIS)  # <-- PUT YOUR FILE PATH HERE

# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container([
    html.H1("Country Crisis Timeline", className='mb-2', style={'textAlign':'center'}),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='select-country',
                value='Argentina',   # default country
                clearable=False,
                options=[{'label': country, 'value': country} for country in sorted(crisis_df['country'].unique())]
            )
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col([
            html.Img(id='timeline-graph', style={'width': '100%'})
        ], width=12)
    ]),
])

# Callback to update timeline
@app.callback(
    Output('timeline-graph', 'src'),
    Input('select-country', 'value')
)
def update_timeline(selected_country):
    df_country = crisis_df[crisis_df['country'] == selected_country].sort_values('year')

    fig, ax = plt.subplots(figsize=(14, 4))
    
    y_pos = [1]*len(df_country)  # Single horizontal line
    ax.scatter(df_country['year'], y_pos, color='#b59e5f', s=100, zorder=3)

    # Add text labels slightly above the points
    for year, event in zip(df_country['year'], df_country['event']):
        ax.text(year, 1.05, event, ha='center', va='bottom', rotation=45, fontsize=8, color='#b59e5f')

    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_ylim(0.8, 1.2)
    ax.set_xlabel('Year', color='#b59e5f')
    ax.set_title(f'Crisis Timeline for {selected_country}', color='#b59e5f')

    ax.set_facecolor('#182225')
    fig.patch.set_facecolor('#182225')
    ax.tick_params(axis='x', colors='#b59e5f')
    ax.spines['bottom'].set_color('#b59e5f')
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()

    # Convert to base64 image
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    fig_data = base64.b64encode(buf.read()).decode("ascii")
    img_src = f'data:image/png;base64,{fig_data}'

    return img_src

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8002)
