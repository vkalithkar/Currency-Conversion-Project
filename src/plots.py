import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def plotly_line(x: np.ndarray, 
                y: np.ndarray) -> go.Figure:
    """
    Given two arrays of data, generate, format, and output a line graph figure. This function is used in creating 
    the exchange rate line graph, so the x-axis is typically years for a certain country and the y-axis is typically 
    exchange rates for that country.

    Arguments:
        x (np.ndarray): array of x-axis data, typically an array of years for a certain country.
        y (np.ndarray): array of y-axis data, typically an array of exchange rates for that country.
    
    Output:
        fig (plots.go.Figure): the properly-formatted Plotly line graph figure object with the relevant data. 
    """
    # Generate basic line graph
    fig = px.line(x=x, y=y)
    
    # Title axes
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Currency Exchange Rate (relative to USD)"
    )

    fig.update_layout(
        # Update figure aesthetics (plot, background, font color)
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(24, 34, 37, 0.7)',
        font=dict(color='#b59e5f'),

        # Update figure aesthetics (gridlines look and color)
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
    
    # Update figure aesthetics (the exchange rate line itself is maroon)
    fig.update_traces(line=dict(color='#280409', width = 4))  

    # Update figure aesthetics (hovering over a data point on the main exchange rate line should give this info)
    fig.update_traces(
        hovertemplate="<b>Year:</b> %{x}<br>" +
                      "<b>Exchange Rate:</b> %{y}<br>" +
                      "<extra></extra>"
    )

    # Update figure aesthetics (generate a horizontal line at y=1 for comparison to an equal exchange rate w/USD)
    fig.add_hline(y=1, annotation_text="Baseline for USD Comparison")

    return fig

# https://plotly.com/python/hover-text-and-formatting/
# https://community.plotly.com/t/hovertemplate-with-customdata-or-hover-data-of-variable-shape/67901
def plotly_scatter(country_crisis_df: pd.DataFrame) -> go.Figure:
    """
    Given two arrays of data, generate, format, and output a scatter graph figure. This function is used in creating 
    the historical event timeline, so the x-axis is typically years for a certain country and the y-axis is 
    typically crisis data for that country.

    Arguments:
        country_crisis_df (pd.DataFrame): the y-axis data, consisting of crisis data for a given country, divided 
                                          into crisis event categorizations.
    
    Output:
        fig (plots.go.Figure): the properly-formatted Plotly scatter graph figure object functioning as a timeline 
                               with the relevant data. 
    """
    # Create a color map for each type of event to separate them by color
    color_map = {
        'Inflation Crisis': '#b59e5f',              # gold
        'Gain of Independence': '#836d65',          # muted tan
        'Gold Standard Adoption': '#006b54',        # muted teal
        'Gold Standard Suspension': '#f5f5f0',      # ivory white
        'Banking Crisis': '#280409',                # maroon
        'Systemic Crisis': '#2a4d69',               # muted blue
        'Currency Crisis': '#7c482b '               # muted orange
    }
    
    # Create a position map on the y axis for each type of event to separate them spatially, 0.1 units apart
    event_y_positions = {
        'Banking Crisis': 1.2,
        'Systemic Crisis': 1.1,
        'Currency Crisis': 1.0,
        'Inflation Crisis': 0.9,
        'Gold Standard Adoption': 0.8,
        'Gold Standard Suspension': 0.7,
        'Gain of Independence': 0.6
    }

    # Map the event positionings onto the y-axis numerical values to apply this change
    country_crisis_df = country_crisis_df.copy()
    country_crisis_df['y_axis'] = country_crisis_df['event'].map(event_y_positions)

    # Use lambda functions to insert even linebreaks so that hovering over each point fits onto the screen
    country_crisis_df['event_notes'] = country_crisis_df['event_notes'].apply(lambda x: insert_linebreaks(x))
    country_crisis_df['domestic_notes'] = country_crisis_df['domestic_notes'].apply(lambda x: insert_linebreaks(x))
    country_crisis_df['external_notes'] = country_crisis_df['external_notes'].apply(lambda x: insert_linebreaks(x))

    # Create basic figure, update axes titles and hover_data, apply color mapping for different events
    fig = px.scatter(country_crisis_df,
                     x = "year",
                     y = 'y_axis',
                     color="event", 
                     hover_data=["event", "event_notes", "domestic_notes", "external_notes"],
                     custom_data = ["event", "event_notes", "domestic_notes", "external_notes"],
                     color_discrete_map=color_map)

    # Update the size of traces
    fig.update_traces(marker=dict(size=12))

    # Update figure aesthetics (event names on the y-axis)
    fig.update_layout(yaxis=dict(
                      title=None,
                      tickvals=list(event_y_positions.values()),
                      ticktext=list(event_y_positions.keys()),
                      showgrid=False),
                      
                      # Update figure aesthetics (colors and muting the legend, takes up too much space)
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(24, 34, 37, 0.7)',
                      font_color='#b59e5f',
                      height=600,
                      xaxis=dict(color='#b59e5f', gridcolor='#b59e5f'),
                      showlegend=False,
                      hoverlabel=dict(align="left")
    )

    # Update figure traces (Rename the data that shows up when hovering over points)
    fig.update_traces(
        marker=dict(size=12),
        hovertemplate="<b>Year:</b> %{x}<br>" +
                      "<b>Event:</b> %{customdata[0]}<br>" +
                      "<b>Event Notes:</b> %{customdata[1]}<br>" +
                      "<b>Domestic notes:</b> %{customdata[2]}<br>" +
                      "<b>External notes:</b> %{customdata[3]}<br>" +
                      "<extra></extra>"
    )

    return fig

def insert_linebreaks(text: str, 
                      char_interval: int = 50) -> str:
    """
    Helper function that takes text input and inserts linebreaks every char_interval number of characters. This 
    function is used to properly space out the text that pops up when the user hovers over the dots in the timeline
    scatter graph.

    Arguments:
        text (str): the text from timeline scatter graph that needs to be formatted.
        char_interval (int): the interval for the number of characters after which to insert a line break, defaults 
                             to 50.
    
    Output:
        text (str): the formatted text with linebreaks to display when the user hovers over the dots in the timeline
                    scatter graph.
    """
    # Check if there is no note info for that data, return blank string to be displayed
    if pd.isna(text):
        return ""
    # Else, join HTML linebreak for each string slice of i to interval for the whole string
    return '<br>'.join(text[i:i+char_interval] for i in range(0, len(text), char_interval))

   
