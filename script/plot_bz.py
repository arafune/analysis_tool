#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import plotly.graph_objects as go
from ase.dft.kpoints import get_special_points
from numpy.typing import NDArray
from plotly.subplots import make_subplots
from scipy.spatial import Delaunay

from eband.bz import get_bz_3d

if __name__ == "__main__":
    #    cell = np.array([[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]])
    cell: NDArray[np.float_] = np.array(
        [
            [3.4690000000, 0.0, 0.0000000000],
            [0.0, 6.3299999237, 0.0000000000],
            [0.0000000000, -0.9467946412, 13.8276234542],
        ]
    )
    icell: NDArray[np.float_] = np.linalg.inv(cell).T
    b1, b2, b3 = np.linalg.norm(icell, axis=1)

    special_kpoints = get_special_points(cell)
    Verts_bz, Edges_bz, Facets_bz = get_bz_3d(icell)

    ############################################################
    fig = go.Figure()
    ############################################################
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

    bz_facet_clrs = [
        "#636EFA",
        "#EF553B",
        "#00CC96",
        "#AB63FA",
        "#FFA15A",
        "#19D3F3",
        "#FF6692",
        "#B6E880",
        "#FF97FF",
        "#FECB52",
    ]
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
                    color="black",
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

            # x, y, z = ff.T
            # fig.add_trace(
            #     go.Mesh3d(
            #         x=x, y=y, z=z,
            #         opacity=0.4,
            #         hoverinfo='skip',
            #         color='blue',
            #         # The alphahull parameter sets the shape of the mesh. If the value
            #         # is -1 (default value) then Delaunay triangulation is used. If >0
            #         # then the alpha-shape algorithm is used. If 0, the convex hull is
            #         # represented (resulting in a convex body).
            #         alphahull=-1,
            #     )
            # )

            # somehow the alphahull does work properly, so I have to resort to the
            # following trick.

            # Add another point outside the facets so that the Delaunay works
            # properly
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
                        # color=bz_facet_clrs[face_clr_id],
                        # color=bz_facet_clrs[fi % len(bz_facet_clrs)],
                        color="gray",
                        i=[0],
                        j=[1],
                        k=[2],
                    )
                )

    ############################################################
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
        xaxis_range=[-0.8, 0.8],
        yaxis_range=[-0.8, 0.8],
        zaxis_range=[-0.8, 0.8],
        xaxis_tickvals=[],
        yaxis_tickvals=[],
        zaxis_tickvals=[],
    )
    # margin=dict(l=0, r=0, t=20, b=20)

    fig.update_layout(
        width=640,
        height=640,
        # margin=margin,
        showlegend=False,
        scene=scene,
    )
    # fig.update_scenes(camera_projection_type='orthographic')
    # fix the ratio in the top left subplot to be a cube
    fig.update_layout(scene_aspectmode="cube")

    fig.write_html("bz.html", include_plotlyjs=False, full_html=False)
    fig.show()
