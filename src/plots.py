import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def plotly_scatter(x: np.ndarray, y: np.ndarray) -> go.Figure:
    fig = px.scatter(x=x, y=y)
    return fig

def plotly_line(x: np.ndarray, y:np.ndarray) -> go.Figure:
    fig = px.line(x=x, y=y)
    return fig