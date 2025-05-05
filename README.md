# The Currency Capsule

The Currency Capsule is a Dash-based web application that provides interactive visualizations and insights into currency exchange rates and their relationship with global historical crises. It allows users to explore historical data, analyze trends in various country exchange rates, and generate custom plots.


## Overview 

This repository contains all the files needed to run **The Currency Capsule**, a data visualization and analysis tool for exploring global currency exchange rates and economic crises.


## Features

* Interactive Dash web application for data visualization.
* Calculates nominal exchange rates of currencies at a time relative to the contemporaneous USD
* Visualizes currency exchange rates and historical crisis data by generating custom plots.
* Easy-to-use interface for exploring datasets.

### Files included in `src/`:

* `main_dash.py`: The entry point of the application. Start here!
* `basicpage.py`: Contains the layout and structure of the Dash application.
* `plots.py`: Handles the creation of interactive plots and visualizations.
* `analysis.py`: Includes functions for data subsetting.
* `assets/`: Contains static assets like CSS and images for the Dash app.

## Quick Start

1. Clone the repository and ensure that dependencies are installed:
   `git clone https://github.com/vkalithkar/Currency-Conversion-Project.git`

2. Run the application:
   `python src/main_dash.py`

3. Click on the link to the local server from the terminal, which should open your browser to the Currency Capsule!
   
   
## Dependencies 

The following Python libraries are required to run **The Currency Capsule**:

1. **numpy**
2. **pandas**
3. **dash**
4. **dash-bootstrap-components**
5. **plotly**
6. **os**

## Author:

Vandana Kalithkar

GitHub: @vkalithkar

[Project Link](https://github.com/vkalithkar/Currency-Conversion-Project.git)

This project is maintained using the [uv package manager](https://docs.astral.sh/uv/).