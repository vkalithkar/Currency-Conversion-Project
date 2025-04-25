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