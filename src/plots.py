import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def plotly_line(x: np.ndarray, y:np.ndarray) -> go.Figure:
    fig = px.line(x=x, y=y)
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Currency Exchange Rate (relative to USD)"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(24, 34, 37, 0.7)',
        font=dict(color='#b59e5f'),

        xaxis=dict(color='#b59e5f', 
                   gridcolor='#b59e5f', 
                   gridwidth=1, 
                   griddash='dot'),
        yaxis=dict(color='#b59e5f', 
                   zeroline=True,
                   zerolinecolor='#b59e5f',
                   zerolinewidth=1, 
                   gridcolor='#b59e5f', 
                   gridwidth=1, 
                   griddash='dot')
    )
    fig.update_traces(line=dict(color='#280409', width = 4))  
    fig.update_traces(
        hovertemplate="<b>Year:</b> %{x}<br>" +
                      "<b>Exchange Rate:</b> %{y}<br>" +
                      "<extra></extra>"
    )
    return fig

# https://plotly.com/python/hover-text-and-formatting/
def plotly_scatter(country_crisis_df) -> go.Figure:
    color_map = {
        'Inflation Crisis': '#280409',     # maroon
        'Gain of Independence': '#008080',    # teal
        'Gold Standard Adoption': '#344756',   # slate
        'Gold Standard Suspension': '#C0C0C0',    # silver
        'Banking Crisis': '#FFDB58',  # Mustard
        'Systemic Crisis': '#36454F',               # black
        'Currency Crisis': '#322a17'
    }
    event_y_positions = {
        'Banking Crisis': 1.2,
        'Systemic Crisis': 1.1,
        'Currency Crisis': 1.0,
        'Inflation Crisis': 0.9,
        'Gold Standard Adoption': 0.8,
        'Gold Standard Suspension': 0.7,
        'Gain of Independence': 0.6
    }

    country_crisis_df = country_crisis_df.copy()
    country_crisis_df['y_axis'] = country_crisis_df['event'].map(event_y_positions)

    country_crisis_df['event_notes'] = country_crisis_df['event_notes'].apply(lambda x: insert_linebreaks(x))
    country_crisis_df['domestic_notes'] = country_crisis_df['domestic_notes'].apply(lambda x: insert_linebreaks(x))
    country_crisis_df['external_notes'] = country_crisis_df['external_notes'].apply(lambda x: insert_linebreaks(x))

    fig = px.scatter(country_crisis_df,
                     x = "year",
                     y = 'y_axis',
                     color="event", 
                     hover_data=["event", "event_notes", "domestic_notes", "external_notes"],
                     color_discrete_map=color_map)

    fig.update_traces(marker=dict(size=12))

    fig.update_layout(yaxis=dict(
                      title=None,
                      tickvals=list(event_y_positions.values()),
                      ticktext=list(event_y_positions.keys()),
                      showgrid=False,
                    #   showticklabels=False
                      ),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(24, 34, 37, 0.7)',
                      font_color='#b59e5f',
                      height=600,
                      xaxis=dict(color='#b59e5f', gridcolor='#b59e5f'),
                      #legend_title_text='Event Type'
                      showlegend=False,
                      hoverlabel=dict(align="left")
    )
    fig.update_traces(
        marker=dict(size=12),
        hovertemplate="<b>Year:</b> %{x}<br>" +
                      "<b>Event:</b> %{customdata[0]}<br>" +
                      "<b>Domestic notes:</b> %{customdata[1]}<br>" +
                      "<b>External notes:</b> %{customdata[2]}<br>" +
                      "<extra></extra>"
    )

    # fig.update_layout(legend=dict(
    #                   yanchor="top",
    #                   y=0.99,
    #                   xanchor="left",
    #                   x=0.01)
    #                   )


    return fig

def insert_linebreaks(text, every=50):
    if isinstance(text, str):
        return '<br>'.join(text[i:i+every] for i in range(0, len(text), every))
    else:
        return text