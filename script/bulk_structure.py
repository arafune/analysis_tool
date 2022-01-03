#!/usr/bin/env python

"""Search for optimized bulk structure in vasp"""

from __future__ import annotations
import os
import math
import pathlib
import glob
import subprocess
from typing import Callable, Optional
import numpy as np
from scipy.optimize import minimize
import argparse


def bianthrone_crystal(vars: tuple[float]) -> None:
    """Generate POSCAR as a function of the single variable.

    Parameters
    -----------
    vars: tuple of float
        variable to be determined.
    """
    output: str = "benc_crystal" + "\n"
    output += str(vars[0]) + "\n"  # change magnification
    output += """       10.1560001373         0.0000000000         0.0000000000
        0.0000000000         8.3649997711         0.0000000000
        -3.8870932354         0.0000000000        10.9707258538
    C    H    O
    56   32   4
Direct
    0.887000024         0.151800007         0.807299972
    0.112999998         0.848199964         0.192700028
    0.612999976         0.651800036         0.692700028
    0.386999995         0.348199993         0.307299972
    0.772799969         0.243699998         0.747099996
    0.227200001         0.756299973         0.252900004
    0.727200031         0.743700027         0.752900004
    0.272799999         0.256300002         0.247099996
    0.740700006         0.275400013         0.623499990
    0.259299994         0.724599957         0.376500010
    0.759299994         0.775400043         0.876500010
    0.240700006         0.224599987         0.123499990
    0.820899963         0.210600004         0.559599996
    0.179100007         0.789399981         0.440400004
    0.679100037         0.710600019         0.940400004
    0.320899993         0.289399981         0.059599996
    0.352100015         0.000400000         0.828100026
    0.647899985         0.999599993         0.171899974
    0.147899985         0.500400007         0.671899974
    0.852100015         0.499599993         0.328100026
    0.456000000         0.031399999         0.779299974
    0.544000030         0.968599975         0.220700026
    0.044000000         0.531400025         0.720700026
    0.955999970         0.468600005         0.279299974
    0.420300007         0.074199997         0.657700002
    0.579699993         0.925800025         0.342299998
    0.079699993         0.574199975         0.842299998
    0.920300007         0.425799996         0.157700002
    0.281699985         0.079200000         0.583500028
    0.718299985         0.920799971         0.416499972
    0.218300015         0.579200029         0.916499972
    0.781700015         0.420800000         0.083500028
    0.101700000         0.004400000         0.812520027
    0.898299992         0.995599985         0.187479973
    0.398299992         0.504400015         0.687479973
    0.601700008         0.495599985         0.312520027
    0.025000000         0.037000000         0.555140018
    0.975000024         0.963000000         0.444859982
    0.474999994         0.537000000         0.944859982
    0.524999976         0.463000000         0.055140018
    0.970200002         0.087899998         0.744109988
    0.029800000         0.912100017         0.255890012
    0.529799998         0.587899983         0.755890012
    0.470200002         0.412100017         0.244109988
    0.935100019         0.112999998         0.617950022
    0.064900003         0.887000024         0.382049978
    0.564899981         0.612999976         0.882049978
    0.435099989         0.386999995         0.117950022
    0.212099999         0.010200000         0.755150020
    0.787899971         0.989799976         0.244849980
    0.287900001         0.510200024         0.744849980
    0.712100029         0.489800006         0.255150020
    0.175500005         0.042399999         0.630140007
    0.824499965         0.957599998         0.369859993
    0.324499995         0.542400002         0.869859993
    0.675500035         0.457599998         0.130140007
    0.912999988         0.130999997         0.893999994
    0.086999997         0.869000018         0.106000006
    0.587000012         0.630999982         0.606000006
    0.412999988         0.369000018         0.393999994
    0.713999987         0.291999996         0.790000021
    0.286000013         0.708000004         0.209999979
    0.786000013         0.791999996         0.709999979
    0.213999987         0.208000004         0.290000021
    0.661000013         0.344999999         0.580999970
    0.338999987         0.654999971         0.419000030
    0.838999987         0.845000029         0.919000030
    0.161000013         0.155000001         0.080999970
    0.796999991         0.234999999         0.472000003
    0.202999994         0.764999986         0.527999997
    0.703000009         0.735000014         0.027999997
    0.296999991         0.264999986         0.972000003
    0.375999987         0.972000003         0.916999996
    0.624000013         0.028000001         0.083000004
    0.124000013         0.472000003         0.583000004
    0.875999987         0.527999997         0.416999996
    0.558000028         0.028999999         0.833000004
    0.441999972         0.971000016         0.166999996
    0.941999972         0.528999984         0.666999996
    0.058000028         0.471000016         0.333000004
    0.493999988         0.100000001         0.621999979
    0.506000042         0.899999976         0.378000021
    0.006000012         0.600000024         0.878000021
    0.993999958         0.400000006         0.121999979
    0.259999990         0.111000001         0.497999996
    0.740000010         0.888999999         0.501999974
    0.240000010         0.611000001         0.002000004
    0.759999990         0.388999999         0.998000026
    0.122910000         0.949900031         0.914539993
    0.877089977         0.050099999         0.085460007
    0.377090007         0.449900001         0.585460007
    0.622910023         0.550099969         0.414539993
    """
    #
    with open("POSCAR", "w") as f:
        f.write(output)


def MoS2(vars: tuple[float, ...]) -> None:
    "Generate POSCAR for MoS2."
    a_axis = float(vars[0])
    c_axis = float(vars[1])
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


def generate_poscar(
    poscar_template: Callable[[tuple[float, ...]], None], coords: tuple[float, ...]
) -> None:
    """Return the POSCAR generate function with arguments.

    Parameters
    -------------
    poscar_template: function
        Function to generate the POSCAR.
        Function must write the POSCAR file as "POSCAR".
        Follow the examples above (MoS2, bianthrone_crystal)
    coords: tuple of float
        arguments of poscar generation function.
    """
    return poscar_template(coords)


# -----------

data: dict[tuple[float, ...], float] = {}


def load_results(
    results: pathlib.Path = pathlib.Path("results.txt"),
) -> dict[tuple[float, ...], float]:
    """Load data from "results.txt".

    Parameters
    ------------
    results: pathlib.Path
        Path object contains "resutls". (Defalut: "results.txt" file)


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
            line_f: tuple[float, ...] = tuple(
                [float(x) for x in s_line.strip().split()]
            )
            data[line_f[:-1]] = line_f[-1]
    return data


def run_vasp() -> str:
    """Run vasp in NIMS super computer.

    Returns
    ---------
    str
        STDOUT of vasp run
    """
    proc: subprocess.CompletedProcess[bytes] = subprocess.run(
        ["mpijob", "/home/arafune/bin/vasp_std_5.4.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return proc.stdout.decode("utf-8")


def fetch_total_energy(coords: tuple[float, ...]|np.ndarray) -> float|None:
    """Return the total energy.

    If the calculaation has already performed with the axis_1 and axis_2
    just return the total energy from the data.

    IF not, vasp run.
    """

    try:
        total_energy = data[tuple(coords)]
    except KeyError:
        generate_poscar(bianthrone_crystal, coords)
        vasp_stdout = run_vasp()
        print(vasp_stdout)
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
        result: str = "".join("{:.6f}  ".format(x) for x in coords)
        result += "".join("{:.6f}\n".format(total_energy))
        results = pathlib.Path("results.txt")
        with results.open(mode="a") as f:
            f.write(result)
    return total_energy


# main routine
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("variables", type=float, nargs="+")
    args = parser.parse_args()
    #
    coords: tuple[float, ...] = tuple(args.variables)
    results = pathlib.Path("results.txt")
    if results.exists():
        data = load_results(results)
        lowest_energy_at: tuple[float, ...] = min(data, key=data.get)
        coords = lowest_energy_at
        lowest = data[lowest_energy_at]
    else:
        lowest = 0

    min_values = minimize(
        fetch_total_energy,
        coords,
        method="nelder-mead",  # Powell method is tested, too. nelder-mead seems to be better.
        options={"xatol": 0.001},
    )
    print(min_values)
