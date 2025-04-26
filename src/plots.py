import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def plotly_line(x: np.ndarray, y:np.ndarray) -> go.Figure:
    fig = px.line(x=x, y=y)
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
    return fig

def plotly_timeline() -> go.Figure:
    df = pd.DataFrame([dict(Task="Argentina Crisis", Start='1981-12-01', Finish='1982-12-31'),
                       dict(Task="Currency Reform", Start='1983-01-01', Finish='1983-06-30')])
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    fig.update_yaxes(autorange="reversed")  
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#b59e5f'),
        xaxis=dict(color='#b59e5f', gridcolor='#b59e5f', gridwidth=1),
        yaxis=dict(color='#b59e5f', gridcolor='#b59e5f', gridwidth=1)
    )
    return fig

def make_crisis_timeline_fig(df: pd.DataFrame) -> px.scatter:
    fig = px.scatter(
        df,
        x="year",
        y="country",
        text="event",
        hover_data=["event_notes", "domestic_notes", "external_notes"],
        title="Historical Crisis Events Timeline",
        labels={"year": "Year", "country": "Country"},
        height=600
    )

    fig.update_traces(marker=dict(size=10), textposition='top center')
    fig.update_layout(
        yaxis=dict(categoryorder='category ascending'),
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='#182225',
        paper_bgcolor='#182225',
        font_color='#b59e5f'
    )

    return fig

def make_argentina_scatter(df):
    color_map = {
        'Inflation Crisis': '#280409',     # Burgundy
        'Gain of Independence': '#008080',    # Teal
        'Gold Standard Adoption': '#344756',   # slate
        'Gold Standard Suspension': '#C0C0C0',    # Silver
        'Banking Crisis': '#FFDB58',  # Mustard
        'Systemic Crisis': '#36454F',               # Charcoal
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

    df = df.copy()
    df['y_axis'] = df['event'].map(event_y_positions)

    fig = px.scatter(df,
                     x = "year",
                     y = 'y_axis',
                     color="event", 
                     hover_data=["event_notes", "domestic_notes", "external_notes"],
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
                      height=550,
                      xaxis=dict(color='#b59e5f', gridcolor='#b59e5f'),
                      #legend_title_text='Event Type'
                      showlegend=False
    )
    # fig.update_layout(legend=dict(
    #                   yanchor="top",
    #                   y=0.99,
    #                   xanchor="left",
    #                   x=0.01)
    #                   )


    return fig
