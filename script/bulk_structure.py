#!/usr/bin/env python

"""Search for optimized bulk structure in vasp"""

import os
import sys
import math
import pathlib
import glob
import subprocess


def fetch_total_energy():
    with open("OSZICAR", "r") as f:
        lines = f.readlines()
    return float(lines[-1].strip().split(" ")[2])


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
    direct = "Direct"
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

    with open("POSCAR", "w") as f:
        f.write(output)


axis_1, step_1, axis_2, step_2, num_i = (
    float(sys.argv[1]),
    float(sys.argv[2]),
    float(sys.argv[3]),
    float(sys.argv[4]),
    int(sys.argv[5]),
)

# find the last iteration number
contcars = glob.glob("./CONTCAR.*")
try:
    lastnum = max([int(i.rsplit(".", 1)[1]) for i in contcars])
except ValueError:
    lastnum = 0
    lowest = 0

results = pathlib.Path("result.txt")
data = {}
if results.exists():
    with results.open(mode="r") as f:
        for s_line in f:
            s_line = s_line.strip().split()
            data[(float(s_line[0]), float(s_line[1]))] = float(s_line[2])
            axis_1 = float(s_line[0])
            axis_2 = float(s_line[1])
        lowest_key = min(data, key=data.get)
        axis_1 = lowest_key[0]
        axis_2 = lowest_key[1]
        lowest = data[lowest_key]
else:
    generate_poscar(axis_1, axis_2)
    proc = subprocess.run(
        ["mpijob", "/home/arafune/bin/vasp_std_5.4.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    lowest = fetch_total_energy()

for i in range(num_i):
    if (i % 2) == 0:
        axis_1 += step_1
    else:
        axis_2 += step_2
    if (axis_1, axis_2) in data:
        continue
    generate_poscar(axis_1, axis_2)
    proc = subprocess.run(
        ["mpijob", "/home/arafune/bin/vasp_std_5.4.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    print(proc.stdout.decode("utf8"))
    total_energy = fetch_total_energy()
    os.rename("OSZICAR", "OSZICAR." + str(lastnum + i))
    os.rename("CONTCAR", "CONTCAR." + str(lastnum + i))
    os.rename("OUTCAR", "OUTCAR." + str(lastnum + i))
    result = "{0}  {1}  {2} \n".format(axis_1, axis_2, total_energy)
    data[(axis_1, axis_2)] = total_energy
    with results.open(mode="a") as f:
        f.write(result)
    if lowest > total_energy:
        lowest = total_energy
    else:
        if (i % 2) == 0:
            axis_1 -= step_1 * 2
            axis_2 -= step_2
        else:
            axis_2 -= step_2 * 2
            axis_1 -= step_1
