#!/usr/bin/env python

"""Search for optimized bulk structure in vasp"""

import os
import sys
import math
import pathlib
import glob
import subprocess


def generate_poscar(a_axis, c_axis):
    "Generate POSCAR for MoS2."
    a_axis = float(a_axis)
    c_axis = float(c_axis)
    system_name = "MoS2"
    mag = 1.0
    axis1 = "  {:8f}  {:.8f}  {:.8f}".format(a_axis, 0, 0)
    axis2 = "  {:8f}  {:.8f}  {:.8f}".format(
        -a_axis / 2, a_axis * math.cos(math.pi / 6), 0
    )
    axis3 = "  {:8f}  {:.8f}  {:.8f}".format(0, 0, c_axis)
    atom_names = "Mo  S"
    atom_nums = "   2  4"
    output = system_name + "\n"
    output += str(mag) + "\n"
    output += axis1 + "\n"
    output += axis2 + "\n"
    output += axis3 + "\n"
    output += atom_names + "\n"
    output += atom_nums + "\n"
    output += "Direct" + "\n"
    output += """    0.666667 0.333333 0.250000
    0.333333 0.666667 0.750000
    0.333333 0.666667 0.144826
    0.666667 0.333333 0.644826
    0.333333 0.666667 0.355174
    0.666667 0.333333 0.855174"""
    #
    with open("POSCAR", "w") as f:
        f.write(output)


# -----------

data = {}


def load_results(results="results.txt"):
    """Load data from "results.txt".

    results.txt
    3.17   12.3  -439.4328
    3.17   12.4  -439.4728
    ...

    The 1st is the value of the "first axis".
    The 2nd is the value of the "second axis"
    The 3rd is the total energy
    """

    with results.open(mode="r") as f:
        for s_line in f:
            s_line = s_line.strip().split()
            data[(float(s_line[0]), float(s_line[1]))] = float(s_line[2])
    return data


def fetch_total_energy(axis_1, axis_2, results="results.txt"):
    """Return the total energy.

    If the calculaation has already performed with the axis_1 and axis_2
    just return the total energy from the data.

    IF not, vasp run.
    """
    try:
        total_energy = data[(axis_1, axis_2)]
    except KeyError:
        # Generate POSCAR
        generate_poscar(axis_1, axis_2)
        # run VASP
        proc = subprocess.run(
            ["mpijob", "/home/arafune/bin/vasp_std_5.4.1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        print(proc.stdout.decode("utf8"))
        # load OSZICAR
        with open("OSZICAR", "r") as f:
            lines = f.readlines()
        total_energy = float(lines[-1].strip().split()[2])
        # Store CONTCAR, OUTCAR, OSZICAR for record.
        contcars = glob.glob("./CONTCAR.*")
        try:
            lastnum = max([int(i.rsplit(".", 1)[1]) for i in contcars])
            os.rename("OSZICAR", "OSZICAR." + str(lastnum + 1))
            os.rename("CONTCAR", "CONTCAR." + str(lastnum + 1))
            os.rename("OUTCAR", "OUTCAR." + str(lastnum + 1))
        except ValueError:
            os.rename("OSZICAR", "OSZICAR.0")
            os.rename("CONTCAR", "CONTCAR.0")
            os.rename("OUTCAR", "OUTCAR.0")
        #
        result = "{0:.6f}  {1:.6f}  {2}\n".format(axis_1, axis_2, total_energy)
        results = pathlib.Path(results)
        with results.open(mode="a") as f:
            f.write(result)
    return total_energy


# main routine
if __name__ == "__main__":
    axis_1, shift_1, axis_2, shift_2, max_i = (
        float(sys.argv[1]),
        float(sys.argv[2]),
        float(sys.argv[3]),
        float(sys.argv[4]),
        int(sys.argv[5]),
    )
    results = pathlib.Path("result.txt")
    if results.exists():
        data = load_results(results)
        lowest_key = min(data, key=data.get)
        axis_1 = lowest_key[0]
        axis_2 = lowest_key[1]
        lowest = data[lowest_key]
    else:
        lowest = 0

    for i in range(max_i):
        current_data = {}
        for current_axes in [
            (axis_1, axis_2),
            (axis_1 + shift_1, axis_2),
            (axis_1 - shift_1, axis_2),
            (axis_1, axis_2 + shift_2),
            (axis_1, axis_2 - shift_2),
        ]:
            energy = fetch_total_energy(current_axes[0], current_axes[1])
            data[(current_axes[0], current_axes[1])] = energy
            try:
                if energy < min(current_data.values()):
                    axis_1 = current_axes[0]
                    axis_2 = current_axes[1]
                    continue
                else:
                    current_data[(current_axes[0], current_axes[1])] = energy
            except ValueError:
                current_data[(current_axes[0], current_axes[1])] = energy
