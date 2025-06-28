import marimo

__generated_with = "0.14.8"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import polars as pl
    import numpy as np
    import matplotlib.pyplot as plt
    from typing import Literal
    from moire_band import energies, potential, HARTREE, EV, A, INV_ANG
    from numpy.typing import NDArray
    return A, INV_ANG, energies, mo, np, pd, pl, plt, potential


@app.cell
def _(A, np):
    kx_vals = np.linspace(0, 2 * np.pi / A, 501)
    kx = kx_vals
    ky = kx_vals
    kxx, kyy = np.meshgrid(kx, ky)
    return (kx_vals,)


@app.cell
def _(pd, pl):
    free_e_bands = pl.from_pandas(
        pd.read_excel("IPS_disp.xlsx", sheet_name="fromFreeEmodel")
    )
    dft_data = pl.from_pandas(
        pd.read_excel("IPS_disp.xlsx", sheet_name="fromDFT", skiprows=0)
    )
    dft_data = dft_data.with_columns(
        (pl.col("k") * 0.1682895289976072 / 2).alias("physical_k")
    )
    free_e_bands = free_e_bands.with_columns(
        (pl.col("k") * 0.1682895289976072 / 2).alias("physical_k")
    )
    return (dft_data,)


@app.cell
def _(mo):
    alpha_ = mo.ui.slider(0, 10, 0.01, label="alpha (meV)", show_value=True)
    beta_ = mo.ui.slider(0, 5, 0.01, label="beta (meV)", show_value=True)
    offset_ = mo.ui.slider(3.9, 4.0, 0.0011, label="offest eV", show_value=True)

    alpha_, beta_, offset_
    return alpha_, beta_, offset_


@app.cell
def _(
    A,
    INV_ANG,
    alpha_,
    beta_,
    dft_data,
    energies,
    kx_vals,
    np,
    offset_,
    plt,
    potential,
):
    fig, ax = plt.subplots(1, 2, figsize=(15, 7))
    ax[0].scatter(
        dft_data["physical_k"] / 0.9787396866295744,
        dft_data["E1"],
        s=14,
        marker="o",
        facecolors="none",
        edgecolors="Blue",
    )
    ax[0].scatter(
        dft_data["physical_k"] / 0.9787396866295744,
        dft_data["E2"],
        s=14,
        marker="o",
        facecolors="none",
        edgecolors="Red",
    )
    ax[0].scatter(
        dft_data["physical_k"] / 0.9787396866295744,
        dft_data["E3"],
        s=14,
        marker="o",
        facecolors="none",
        edgecolors="Green",
    )
    bands_along_kx = np.array(
        [
            energies(kx, 0, alpha_.value, beta_.value, lattice_const_bohr=A)
            for kx in kx_vals
        ]
    )
    for _ in range(3):
        ax[0].plot(kx_vals * INV_ANG, bands_along_kx[:, _] + offset_.value)
    ax[0].set_xlim(-0.01, 0.27)
    ax[0].set_ylim(offset_.value - 0.01, 4.1)

    xmax = 1.5
    ymax = np.sqrt(3) / 2
    division = 100
    X = np.linspace(0, xmax, division)
    Y = np.linspace(0, ymax, division)
    xx, yy = np.meshgrid(X, Y)
    z = potential(xx, yy, alpha_.value, beta_.value)
    ax[1].imshow(
        z, origin="lower", aspect=1, extent=[0, xmax, 0, ymax], cmap="RdBu_r"
    )
    ax[1].set_xlabel("x/a")
    ax[1].set_ylabel("y/a")
    fig
    return


@app.cell
def _(mo):
    mo.md(r"""$\alpha=8.01$, $\beta=0.95$, offset=3.9308 is fine.""")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
