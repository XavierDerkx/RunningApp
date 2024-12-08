#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RunningApp."""

__author__ = "Xavier Derkx"
__copyright__ = "Copyright 2024"
__credits__ = ["Xavier Derkx"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Xavier Derkx"
__email__ = "[email protected]"
__status__ = "Prototype"

import math
from pathlib import Path
import json

from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import plotly.express as px

from data_source_factory import DataSourceFactory, DataType
from data_source import DataSource
from analyser import AnalyserFactory, Analyser


def main():
    """Call the main function."""
    SOURCE_PATH = Path("./sample/")
    SOURCE_FILES = [
        Path(".", SOURCE_PATH, "ACT_0000DATA1.csv"),
        ]

    ds = DataSourceFactory.create_data_source(data_type=DataType.ON_MOVE,
                                              files=[SOURCE_FILES[0]])

    analyser = AnalyserFactory.create_analyser(ds)
    analyser.summary

    dashboard(ds, analyser)


def dashboard(ds: DataSource, analyser):
    """Test for the dashboard."""
    # -------------------------------------------------------------------------
    latitude = "Latitude"
    longitude = "Longitude"

    map_centre = ds.run_centre
    # TODO Deduce the scalefactor from the screen resolution.
    # Check documentation: link between zoom and degres for Lat and Long?
    scale_factor = 160
    map_zoom = math.ceil(ds.run_width * scale_factor)

    pos = ds.dataframe[[latitude, longitude]].values.tolist()
    positions = [(lat, lon) for lat, lon in pos]

    STYLE_SHEETS = [dbc.themes.PULSE]
    PAGE_SIZE = 10
    # Dirty fix for the analyser to be known in the callback
    global ANALYSER
    ANALYSER = analyser
    # -------------------------------------------------------------------------
    app = Dash(external_stylesheets=STYLE_SHEETS)
    app.layout = [
        html.Div(children="RunningApp"),
        # ---------------------------------------------------------------------
        # Data
        html.H3("Data"),
        dash_table.DataTable(data=ds.dataframe.to_dict("records"),
                             page_size=PAGE_SIZE),
        html.Hr(),
        # ---------------------------------------------------------------------
        # Summary
        html.H3("Summary"),
        html.Article(json.dumps(analyser.summary, default=str)),
        html.Hr(),
        # ---------------------------------------------------------------------
        # Plots
        html.H3("Plot"),
        dcc.Dropdown(id='demo-dropdown',
                     options=[{'label': k, 'value': k}
                              for k in Analyser.kpi()],
                     value='Minute',
                     style={'width': '50%', 'display': 'inline-block'},
                     multi=False),
        dcc.Graph(id='display-selected-values'),
        html.Hr(),
        # ---------------------------------------------------------------------
        # Map
        html.H3("Map"),
        dl.Map([dl.TileLayer(), dl.Polyline(positions=positions)],
               center=map_centre, zoom=map_zoom,
               style={'height': '50vh', 'color': 'red'}),
        html.Div(id='summary-show')
        ]

    DEBUG = True
    PORT = 8057
    app.run(debug=DEBUG, port=PORT)


@callback(
    Output('display-selected-values', 'figure'),
    Input('demo-dropdown', 'value'))
def update_output(data):
    """Callbacks."""
    df = ANALYSER.compress_by(data)
    fig = px.line(df, x=data, y="Speed",
                  title=f"{data} vs Speed")
    # fig.show()
    return fig


if __name__ == "__main__":
    main()
