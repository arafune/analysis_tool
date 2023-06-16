#!/usr/bin/env python3
"""Plot pressure log of phoibos system"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def load_log(file_name: str | Path) -> tuple[list[datetime], list[tuple[float]]]:
    date_time: list[datetime] = []
    data: list[list[float]] = []
    with open(file_name, mode="r") as f:
        for line in f:
            tmp = line.split("\t")
            date_time.append(datetime.strptime(tmp.pop(0), "%Y/%m/%d %H:%M:%S.%f"))
            data.append([float(i) for i in tmp])
    return date_time, list(zip(*data))


def plotting(
    date_time: list[datetime],
    data: list[tuple[float]],
    ignores: list[str] = [],
) -> Figure:
    fig: Figure = plt.figure(figsize=(8.2, 11.9))
    num_plots: int = 5
    if ("pres_a" in ignores) and ("pres_p" in ignores):
        num_plots = num_plots - 1
    elif ("i_fil" in ignores) and ("v_fil" in ignores):
        num_plots = num_plots - 1
    elif ("i_e" in ignores) and ("high_v" in ignores):
        num_plots = num_plots - 1
    elif "t_pyro" in ignores:
        num_plots = num_plots - 1
    elif "t_tc" in ignores:
        num_plots = num_plots - 1
    #
    axs: list[plt.Axes] = []
    i = 0
    num_graphs = 1
    if "pres_p" not in ignores:
        axs.append(fig.add_subplot(num_plots, 1, num_graphs))
        num_graphs += 1
        axs[i].plot(date_time, data[0], label="Pressure (Preparation)")
        axs[i].set_yscale("log")
        axs[i].set_ylabel("Pressure  ( mbar )")
        axs[i].grid(True)
        axs[i].legend()
    if "pres_a" not in ignores:
        if len(axs) == 0:
            axs.append(fig.add_subplot(num_plots, 1, num_graphs))
            num_graphs += 1
        axs[i].plot(date_time, data[1], label="Pressure (Analysis)")
        axs[i].set_yscale("log")
        axs[i].set_ylabel("Pressure  ( mbar )")
        axs[i].legend()
    if len(axs) == 1:
        i += 1
    if "filament" not in ignores:
        axs.append(fig.add_subplot(num_plots, 1, num_graphs, sharex=axs[0]))
        num_graphs += 1
        vfil = axs[i].plot(date_time, data[2], c="orange", label="V_fil")
        axs[i].set_ylabel("Voltage (V)")
        axs[i].grid(True)
        axs.append(axs[i].twinx())
        i += 1
        ifil = axs[i].plot(date_time, data[3], label="I_fil")
        axs[i].set_ylabel("Current  (A)")

        axs[i].legend(ifil + vfil, [l.get_label() for l in ifil + vfil])
        i += 1
    if "highvol" not in ignores:
        axs.append(fig.add_subplot(num_plots, 1, num_graphs, sharex=axs[0]))
        num_graphs += 1
        hv = axs[i].plot(date_time, data[4], c="orange", label="HV")
        axs[i].set_ylabel("Voltage (V)")
        axs[i].grid(True)
        axs.append(axs[i].twinx())
        i += 1
        ie = axs[i].plot(date_time, data[5], label="I_e")
        axs[i].set_ylabel("Current  (mA)")
        axs[i].legend(ie + hv, [l.get_label() for l in ie + hv])
        i += 1
    if "pyro" not in ignores:
        axs.append(fig.add_subplot(num_plots, 1, num_graphs, sharex=axs[0]))
        num_graphs += 1
        axs[i].plot(date_time, data[6], label="T_pyrometer")
        axs[i].set_ylabel("Temperature  (C)")
        axs[i].grid(True)
        axs[i].legend()
        i += 1
    if "tc" not in ignores:
        axs.append(fig.add_subplot(num_plots, 1, num_graphs, sharex=axs[0]))
        num_graphs += 1
        axs[i].plot(date_time, data[7], label="T_thermocouple")
        axs[i].set_ylabel("Temperature  (C)")
        axs[i].grid(True)
        axs[i].legend()
        i += 1
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ignore",
        type=str,
        help="""Ignore item(s). Separated by comma.
        ignores: canbe
        pres_a, pres_p, filament, highvol, pyro, tc
        """,
    )
    parser.add_argument("logfile", help="Log file name")
    args = parser.parse_args()

    """data contains

    pressure_p, pressur_a, filament, highvol, pyro, tc
    """
    if args.ignore is None:
        ignores = []
    else:
        ignores = args.ignore.split(",")

    logfile = Path(args.logfile)
    date_time, data = load_log(logfile)
    #
    fig: Figure = plotting(date_time, data, ignores=ignores)
    fig.suptitle(logfile.stem)
    fig.savefig(logfile.stem + ".pdf", dpi=600)
