"""Helper function for pyarpes.

At present, the functions are for privately use.
"""

import matplotlib.pyplot as plt
import xarray as xr
from arpes.plotting.utils import fancy_labels
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def short_summay(data_all: list[xr.DataArray], ncols: int = 3) -> tuple[Figure, Axes]:
    """Build fig and axes to summarize the ARPES data.

    Parameters
    ----------
    data_all
        [TODO:description]
    ncols
        [TODO:description]

    Returns
    -------

    Figure, Axes
        Summarized figures.
    """
    num_figs = len(data_all)
    nrows = num_figs // ncols
    if num_figs % ncols:
        nrows += 1
    fig: Figure = plt.figure(figsize=(3 * ncols, 3 * nrows))
    ax: list[Axes] = []
    for i, spectrum in enumerate(data_all):
        ax.append(fig.add_subplot(nrows, ncols, i + 1))
        spectrum.S.transpose_to_front("eV").plot(
            ax=ax[i],
            add_labels=False,
            add_colorbar=False,
        )
        ax[i].text(
            0.01,
            0.91,
            f"ID:{spectrum.id}",
            color="white",
            transform=ax[i].transAxes,
        )
        fancy_labels(ax[i])
    return fig, ax
