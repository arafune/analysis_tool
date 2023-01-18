#! /usr/bin/env python3


from __future__ import annotations

import dash
import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from scipy.spatial import Delaunay

from eband.bz import get_bz_3d

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Draw Brillouin zone",
    suppress_callback_exceptions=True,
)


def input_for_lattice(index: int, axis: str):
    return dcc.Input(
        id=f"a{index}_{axis}",
        type="number",
        debounce=True,
        placeholder=f"a{index}_{axis}",
        value=0,
    )


draw_bz_button = html.Button("Draw BZ", id="draw_bz_button", n_clicks=0)


def make_a_axis(id: int):
    return html.Div(
        [
            html.P(f"a{id}"),
            input_for_lattice(id, "x"),
            input_for_lattice(id, "y"),
            input_for_lattice(id, "z"),
        ]
    )


reciprocal_lattice = html.P(id="reciprocal")
magnification = dcc.Input(
    id="magnification", type="number", debounce=True, value=2, min=0.5
)


app.layout = html.Div(
    [
        make_a_axis(1),
        make_a_axis(2),
        make_a_axis(3),
        # html.Div([draw_bz_button, magnification]),
        draw_bz_button,
        reciprocal_lattice,
        dcc.Graph(id="bz_graph"),
    ]
)


@app.callback(
    Output("reciprocal", "children"),
    Output("bz_graph", "figure"),
    State("a1_x", "value"),
    State("a1_y", "value"),
    State("a1_z", "value"),
    State("a2_x", "value"),
    State("a2_y", "value"),
    State("a2_z", "value"),
    State("a3_x", "value"),
    State("a3_y", "value"),
    State("a3_z", "value"),
    # State("magnification", "value"),
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
    # mag: float,
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
    range_value = np.max(np.abs(Verts_bz)) * 1.2
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
    fig = go.Figure()
    # plot the basis
    basis_clrs = ["red", "green", "blue"]
    basis_labs = [r"b<sub>{}</sub>".format(ii + 1) for ii in range(3)]
    for ii, basis in enumerate(icell):
        bx, by, bz = basis
        fig.add_trace(
            go.Scatter3d(
                x=[0, bx],
                y=[0, by],
                z=[0, bz],
                opacity=0.8,
                hoverinfo="skip",
                mode="lines+text",
                line=dict(
                    color=basis_clrs[ii],
                    width=6,
                ),
                text=["", basis_labs[ii]],
                textfont=dict(color=basis_clrs[ii], size=20),
            )
        )

    for shift in np.array(
        [
            [0, 0, 0],
            # 2 * np.dot(special_kpoints["E"], icell),
        ]
    ):
        sx, sy, sz = shift
        # the vertices
        fig.add_trace(
            go.Scatter3d(
                x=Verts_bz[:, 0] + sx,
                y=Verts_bz[:, 1] + sy,
                z=Verts_bz[:, 2] + sz,
                opacity=0.8,
                hoverinfo="skip",
                mode="markers",
                marker=dict(
                    color="blue",
                    size=6,
                ),
            )
        )

        # the edges
        for l in Edges_bz:
            x, y, z = (l + shift).T
            fig.add_trace(
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    opacity=0.8,
                    hoverinfo="skip",
                    mode="lines",
                    line=dict(
                        color="black",
                        width=5,
                    ),
                )
            )
        # the facets
        edges_of_facets = list(np.sort(np.unique([len(ff) for ff in Facets_bz])))
        for fi, ff in enumerate(Facets_bz):
            face_clr_id = edges_of_facets.index(len(ff))
            simplex_g = np.vstack([[0, 0, 0], ff])
            tri = Delaunay(simplex_g)
            for ii, xx in enumerate(tri.simplices):
                # exclude the extra point when plotting faces
                x, y, z = simplex_g[xx[xx != 0]].T
                fig.add_trace(
                    go.Mesh3d(
                        x=x + sx,
                        y=y + sy,
                        z=z + sz,
                        opacity=0.3,
                        hoverinfo="skip",
                        color="gray",
                        i=[0],
                        j=[1],
                        k=[2],
                    )
                )

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.00, y=-1.20, z=0.00),
    )
    scene = dict(
        camera=camera,
        xaxis_showbackground=False,
        yaxis_showbackground=False,
        zaxis_showbackground=False,
        xaxis_title="",
        yaxis_title="",
        zaxis_title="",
        xaxis_range=[-range_value, range_value],
        yaxis_range=[-range_value, range_value],
        zaxis_range=[-range_value, range_value],
        xaxis_tickvals=[],
        yaxis_tickvals=[],
        zaxis_tickvals=[],
    )
    fig.update_layout(
        width=640,
        height=640,
        showlegend=False,
        scene=scene,
    )
    # fig.update_scenes(camera_projection_type='orthographic')
    # fix the ratio in the top left subplot to be a cube
    fig.update_layout(scene_aspectmode="cube")
    return icell_str, fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
