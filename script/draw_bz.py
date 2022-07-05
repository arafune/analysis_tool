#! /usr/bin/env python3


from __future__ import annotations
from typing import Literal
import unittest
import dash
from dash import dcc, html, Input, Output, State
import dash_daq as daq
import plotly.graph_objects as go
import tempfile
import shutil
from pathlib import Path
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scipy.spatial import Delaunay

from eband.bz import get_bz_3d


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Draw Brillouin zone",
    suppress_callback_exceptions=True,
)


a1_x_input = dcc.Input(
    id="a1_x", type="number", debounce=True, placeholder="a1_x", value=0
)
a1_y_input = dcc.Input(
    id="a1_y", type="number", debounce=True, placeholder="a1_y", value=0.5
)
a1_z_input = dcc.Input(
    id="a1_z", type="number", debounce=True, placeholder="a1_z", value=0.5
)
a2_x_input = dcc.Input(
    id="a2_x", type="number", debounce=True, placeholder="a2_x", value=0.5
)
a2_y_input = dcc.Input(
    id="a2_y", type="number", debounce=True, placeholder="a2_y", value=0
)
a2_z_input = dcc.Input(
    id="a2_z", type="number", debounce=True, placeholder="a2_z", value=0.5
)
a3_x_input = dcc.Input(
    id="a3_x", type="number", debounce=True, placeholder="a3_x", value=0.5
)
a3_y_input = dcc.Input(
    id="a3_y", type="number", debounce=True, placeholder="a3_y", value=0.5
)
a3_z_input = dcc.Input(
    id="a3_z", type="number", debounce=True, placeholder="a3_z", value=0
)
#
draw_bz_button = html.Button("Draw BZ", id="draw_bz_button", n_clicks=0)


a1 = html.Div([a1_x_input, a1_y_input, a1_z_input])
a2 = html.Div([a2_x_input, a2_y_input, a2_z_input])
a3 = html.Div([a3_x_input, a3_y_input, a3_z_input])

reciprocal_lattice = html.P(id="reciprocal")

app.layout = html.Div([a1, a2, a3, draw_bz_button, reciprocal_lattice])


@app.callback(
    Output("reciprocal", "children"),
    State("a1_x", "value"),
    State("a1_y", "value"),
    State("a1_z", "value"),
    State("a2_x", "value"),
    State("a2_y", "value"),
    State("a2_z", "value"),
    State("a3_x", "value"),
    State("a3_y", "value"),
    State("a3_z", "value"),
    Input("draw_bz_button", "n_clicks"),
)
def update_reciprocal(
    a1_x: float,
    a1_y: float,
    a1_z: float,
    a2_x: float,
    a2_y: float,
    a2_z: float,
    a3_x: float,
    a3_y: float,
    a3_z: float,
    nclicks: int,
) -> str:
    cell = np.array(
        [
            [a1_x, a1_y, a1_z],
            [a2_x, a2_y, a2_z],
            [a3_x, a3_y, a3_z],
        ]
    )
    icell = np.linalg.inv(cell).T
    b1, b2, b3 = np.linalg.norm(icell, axis=1)
    # special_kpoints = get_special_points(cell)
    Verts_bz, Edges_bz, Facets_bz = get_bz_3d(icell)
    icell_str = "{} {} {} \n{} {} {}\n{} {} {}\n".format(
        icell[0][0],
        icell[1][0],
        icell[2][0],
        icell[0][1],
        icell[1][1],
        icell[2][1],
        icell[0][2],
        icell[1][2],
        icell[2][2],
    )
    return icell_str


fig = go.Figure()


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
