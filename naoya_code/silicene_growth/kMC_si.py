#!/usr/bin/env python3

import numpy as np
import copy
import math
import time
import tkinter
from typing import List, Dict
import tkinter as tk
from tkinter import ttk
import os
import random
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.lines as mlines
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageGrab
from pptx import Presentation
from pptx.util import Inches, Pt


input_params: Dict[str, float] = {}


def update_values():
    global pre
    pre = float(entry_pre.get())
    # calculate deposition speed
    nl = int(entry_1.get())
    d_rate = float(entry_rate.get())  # ML/min
    d_rate = d_rate / 60  # ML/s
    NBL = 2 * nl * nl  # atoms/ML
    d_rate = d_rate * NBL  # atoms/s

    text_AgSi_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_AgSi.get()))))
    text_Si12_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_Si12.get()))))
    text_Si23_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_Si23.get()))))
    text_Si34_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_Si34.get()))))
    text_Si45_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_Si45.get()))))
    text_Si56_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_Si56.get()))))
    text_Siel_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_Siel.get()))))
    text_Sielin_rates["text"] = str(
        "{:.5f}".format(cal_rate(float(entry_Sielin.get())))
    )
    text_Agtp_rates["text"] = str("{:.5f}".format(cal_rate(float(entry_Agtp.get()))))
    text_ats["text"] = str("{:.5f}".format(d_rate))
    root.update()


def update(event):
    update_values()


def show_current():
    global atom_set, lattice, c_num, max_layer
    print("current saving")
    # image
    fig = plt.figure()
    ax = fig.add_subplot(111)
    length = nl
    p = pat.Polygon(
        xy=[
            (0, 0),
            (unit_x[0] * length, unit_x[1] * length),
            ((unit_x[0] + unit_y[0]) * length, (unit_x[1] + unit_y[1]) * length),
            (unit_y[0] * length, unit_y[1] * length),
        ],
        fc=(0.5, 0.5, 0.5),
        ec=(0, 0, 0),
    )
    ax.add_patch(p)
    atom_set_n = atom_set
    for z in range(0, max_layer):
        for i in range(len(atom_set_n)):
            for k in range(len(atom_set_n[i])):
                if atom_set_n[i][k][z] == 0:
                    pass
                else:
                    xp = lattice[i][k][z][0]
                    yp = lattice[i][k][z][1]
                    zp = lattice[i][k][z][2]

                    if z % 2 == 0:
                        t1x = (
                            xp * unit_x[0]
                            + yp * unit_y[0]
                            - (unit_x[0] + unit_y[0]) / 3
                        )
                        t1y = (
                            xp * unit_x[1]
                            + yp * unit_y[1]
                            - (unit_x[1] + unit_y[1]) / 3
                        )
                        t2x = t1x + unit_x[0]
                        t2y = t1y + unit_x[1]
                        t3x = t1x + unit_y[0]
                        t3y = t1y + unit_y[1]
                    else:
                        t1x = (
                            xp * unit_x[0]
                            + yp * unit_y[0]
                            + (unit_x[0] + unit_y[0]) / 3
                        )
                        t1y = (
                            xp * unit_x[1]
                            + yp * unit_y[1]
                            + (unit_x[1] + unit_y[1]) / 3
                        )

                        t2x = t1x - unit_x[0]
                        t2y = t1y - unit_x[1]

                        t3x = t1x - unit_y[0]
                        t3y = t1y - unit_y[1]

                    color_num = math.floor(z / 2) * 2
                    if z == 1 or z == 0:
                        color = [0, 1, 0]
                    else:
                        color = [color_num / max_layer, 0, 1 - color_num / max_layer]

                    p = pat.Polygon(
                        xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                    )

                    ax.add_patch(p)

                    if i == 0:
                        if z % 2 == 0:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                - (unit_x[0] + unit_y[0]) / 3
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                - (unit_x[1] + unit_y[1]) / 3
                                + unit_x[1] * length
                            )

                            t2x = t1x + unit_x[0]
                            t2y = t1y + unit_x[1]

                            t3x = t1x + unit_y[0]
                            t3y = t1y + unit_y[1]
                        else:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                + (unit_x[0] + unit_y[0]) / 3
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                + (unit_x[1] + unit_y[1]) / 3
                                + unit_x[1] * length
                            )

                            t2x = t1x - unit_x[0]
                            t2y = t1y - unit_x[1]

                            t3x = t1x - unit_y[0]
                            t3y = t1y - unit_y[1]

                        p = pat.Polygon(
                            xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                        )
                        ax.add_patch(p)

                    if k == 0:
                        if z % 2 == 0:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                - (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                - (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                            )

                            t2x = t1x + unit_x[0]
                            t2y = t1y + unit_x[1]

                            t3x = t1x + unit_y[0]
                            t3y = t1y + unit_y[1]
                        else:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                + (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                + (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                            )

                            t2x = t1x - unit_x[0]
                            t2y = t1y - unit_x[1]

                            t3x = t1x - unit_y[0]
                            t3y = t1y - unit_y[1]

                        p = pat.Polygon(
                            xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                        )
                        ax.add_patch(p)

                    if (i == 0) and (k == 0):

                        if z % 2 == 0:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                - (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                - (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                                + unit_x[1] * length
                            )

                            t2x = t1x + unit_x[0]
                            t2y = t1y + unit_x[1]

                            t3x = t1x + unit_y[0]
                            t3y = t1y + unit_y[1]
                        else:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                + (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                + (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                                + unit_x[1] * length
                            )

                            t2x = t1x - unit_x[0]
                            t2y = t1y - unit_x[1]

                            t3x = t1x - unit_y[0]
                            t3y = t1y - unit_y[1]

                        p = pat.Polygon(
                            xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                        )
                        ax.add_patch(p)
    p = pat.Polygon(
        xy=[(0, 0), (unit_y[0] * length, unit_y[1] * length), (0, unit_y[1] * length)],
        fc=(1, 1, 1),
        ec=(0, 0, 0),
    )
    ax.add_patch(p)
    p = pat.Polygon(
        xy=[
            (unit_x[0] * length, 0),
            ((unit_x[0] + unit_y[0]) * length, 0),
            ((unit_x[0] + unit_y[0]) * length, (unit_x[1] + unit_y[1]) * length),
        ],
        fc=(1, 1, 1),
        ec=(0, 0, 0),
    )
    ax.add_patch(p)
    ax.set_xlim(0, (unit_x[0] + unit_y[0]) * length)
    ax.set_ylim(0, (unit_x[1] + unit_y[1]) * length)
    ax.set_aspect("equal")
    file_name = entry_rec.get() + "_current_" + str(c_num) + ".png"
    fig.savefig(file_name)

    # poscar

    xp = []
    yp = []
    zp = []
    num = 0
    s = atom_set

    for i in range(len(s)):
        for k in range(len(s[i])):
            for z in range(len(s[i][k])):
                if s[i][k][z] != 0:
                    xp.append(lattice[i][k][z][0] / nl)
                    yp.append(lattice[i][k][z][1] / nl)
                    zp.append(lattice[i][k][z][2] / zl / 2.448)
                    num = num + 1

    file_name = entry_rec.get() + "_" + "current" + str(c_num) + ".vasp"
    file_data = open(file_name, "w")
    file_data.write(entry_rec.get() + "\n")
    file_data.write("10" + "\n")
    file_data.write(str(nl) + "\t" + "0" + "\t" + "0" + "\n")
    file_data.write(str(nl / 2) + "\t" + str(nl / 2 * 1.732) + "\t" + "0" + "\n")
    file_data.write("0" + "\t" + "0" + "\t" + str(zl * 2.448) + "\n")
    file_data.write("Si" + "\n")
    file_data.write(str(num) + "\n")
    file_data.write("direct" + "\n")
    for i in range(len(xp)):
        file_data.write(str(xp[i]) + "\t" + str(yp[i]) + "\t" + str(zp[i]) + "\n")
    file_data.close()
    c_num = c_num + 1


def lattice_form():
    global lattice, atom_set, bonds, nl, zl, event, event_time, event_tot, maxz, max_atom
    nl = int(entry_1.get())
    zl = int(entry_zunit.get())
    lattice_first = []
    lattice = []
    atom_set = []
    bonds = []
    event = []
    event_tot = []
    event_time = []
    maxz = 0
    # Calculating the position of atoms in the first unit in z (first 3 BL)
    for i in range(0, nl):
        lattice.append([])
        lattice_first.append([])
        atom_set.append([])
        bonds.append([])
        event.append([])
        event_tot.append([])
        event_time.append([])
        for k in range(0, nl):
            lattice[-1].append([])
            lattice_first[-1].append([])
            atom_set[-1].append([])
            bonds[-1].append([])
            event[-1].append([])
            event_tot[-1].append([])
            event_time[-1].append([])

            unit_pos = [i, k, 0]  # coodination of the unit cell
            # 6 atoms in a unit in z direction
            # first BL
            atom1 = [unit_pos[0], unit_pos[1], unit_pos[2]]
            atom2 = [atom1[0] + 0.333, atom1[1] + 0.333, atom1[2] + zd1]
            # second BL
            atom3 = [atom2[0], atom2[1], atom2[2] + zd2]
            atom4 = [atom3[0] + 0.334, atom3[1] + 0.334, atom3[2] + zd1]
            # Third BL
            atom5 = [atom4[0], atom4[1], atom4[2] + zd2]
            atom6 = [atom1[0], atom1[1], atom5[2] + zd1]

            # latice_first: coodination of all atoms
            # lattice_num_first: numerization of atoms
            lattice_first[-1][-1].extend([atom1, atom2, atom3, atom4, atom5, atom6])

    # Calculating the position of all atoms
    for i in range(len(lattice_first)):
        for k in range(len(lattice_first[i])):
            for u in range(0, zl):
                for z in range(len(lattice_first[i][k])):
                    lattice[i][k].append(
                        [
                            round(lattice_first[i][k][z][0], 5),
                            round(lattice_first[i][k][z][1], 5),
                            round(lattice_first[i][k][z][2] + u * 2.448, 5),
                        ]
                    )

                    atom_set[i][k].append(0)
                    event[i][k].append([])
                    event_time[i][k].append([])
                    event_tot[i][k].append(0)

    # lattice: coodination of an atom at [i,k,z]
    maxz = len(lattice[0][0]) - 1
    max_atom = maxz * nl * nl

    # Search for bonding atoms for all the atoms
    for i in range(len(lattice)):
        for k in range(len(lattice[i])):
            for z in range(len(lattice[i][k])):
                bonds_t = []
                zv = int(z % 6)
                ml = nl - 1
                if zv == 0:
                    if i == 0 and k == 0:
                        bonds_t = [[ml, 0, z + 1], [0, ml, z + 1], [0, 0, z + 1]]
                    elif i == 0:
                        bonds_t = [[ml, k, z + 1], [0, k - 1, z + 1], [0, k, z + 1]]
                    elif k == 0:
                        bonds_t = [[i - 1, 0, z + 1], [i, ml, z + 1], [i, 0, z + 1]]
                    else:
                        bonds_t = [[i - 1, k, z + 1], [i, k - 1, z + 1], [i, k, z + 1]]
                    if z != 0:
                        bonds_t.append([i, k, z - 1])
                    else:
                        pass
                elif zv == 1:
                    if i == ml and k == ml:
                        bonds_t = [[ml, 0, z - 1], [0, ml, z - 1], [ml, ml, z - 1]]
                    elif i == ml:
                        bonds_t = [[ml, k + 1, z - 1], [0, k, z - 1], [ml, k, z - 1]]
                    elif k == ml:
                        bonds_t = [[i + 1, ml, z - 1], [i, 0, z - 1], [i, ml, z - 1]]
                    else:
                        bonds_t = [[i + 1, k, z - 1], [i, k + 1, z - 1], [i, k, z - 1]]
                    bonds_t.append([i, k, z + 1])
                elif zv == 2:
                    if i == 0 and k == 0:
                        bonds_t = [[ml, 0, z + 1], [0, ml, z + 1], [0, 0, z + 1]]
                    elif i == 0:
                        bonds_t = [[ml, k, z + 1], [0, k - 1, z + 1], [0, k, z + 1]]
                    elif k == 0:
                        bonds_t = [[i - 1, 0, z + 1], [i, ml, z + 1], [i, 0, z + 1]]
                    else:
                        bonds_t = [[i - 1, k, z + 1], [i, k - 1, z + 1], [i, k, z + 1]]
                    bonds_t.append([i, k, z - 1])
                elif zv == 3:
                    if i == ml and k == ml:
                        bonds_t = [[ml, 0, z - 1], [0, ml, z - 1], [ml, ml, z - 1]]
                    elif i == ml:
                        bonds_t = [[ml, k + 1, z - 1], [0, k, z - 1], [ml, k, z - 1]]
                    elif k == ml:
                        bonds_t = [[i + 1, ml, z - 1], [i, 0, z - 1], [i, ml, z - 1]]
                    else:
                        bonds_t = [[i + 1, k, z - 1], [i, k + 1, z - 1], [i, k, z - 1]]
                    bonds_t.append([i, k, z + 1])
                elif zv == 4:
                    if i == ml and k == ml:
                        bonds_t = [[ml, 0, z + 1], [0, ml, z + 1], [0, 0, z + 1]]
                    elif i == ml:
                        bonds_t = [[0, k, z + 1], [0, k + 1, z + 1], [ml, k + 1, z + 1]]
                    elif k == ml:
                        bonds_t = [[i + 1, 0, z + 1], [i, 0, z + 1], [i + 1, ml, z + 1]]
                    else:
                        bonds_t = [
                            [i + 1, k, z + 1],
                            [i + 1, k + 1, z + 1],
                            [i, k + 1, z + 1],
                        ]
                    bonds_t.append([i, k, z - 1])
                elif zv == 5:
                    if i == 0 and k == 0:
                        bonds_t = [[ml, ml, z - 1], [0, ml, z - 1], [ml, 0, z - 1]]
                    elif i == 0:
                        bonds_t = [
                            [0, k - 1, z - 1],
                            [ml, k, z - 1],
                            [ml, k - 1, z - 1],
                        ]
                    elif k == 0:
                        bonds_t = [
                            [i, ml, z - 1],
                            [i - 1, ml, z - 1],
                            [i - 1, 0, z - 1],
                        ]
                    else:
                        bonds_t = [
                            [i - 1, k, z - 1],
                            [i, k - 1, z - 1],
                            [i - 1, k - 1, z - 1],
                        ]
                    bonds_t.append([i, k, z + 1])
                bonds[i][k].append(bonds_t)


def lattice_form_check():
    global lattice, atom_set, bonds, nl, zl

    lattice_form()

    min_x = -1
    max_x = (unit_x[0] + unit_y[0]) * nl + 1
    min_y = -1
    max_y = (unit_x[1] + unit_y[1]) * nl + 1

    x = []
    y = []
    b = []

    for z in range(len(lattice[0][0])):
        x.append([])
        y.append([])
        b.append([])

        for i in range(len(lattice)):
            for k in range(len(lattice[i])):
                xp = lattice[i][k][z][0] * unit_x[0] + lattice[i][k][z][1] * unit_y[0]
                yp = lattice[i][k][z][0] * unit_x[1] + lattice[i][k][z][1] * unit_y[1]

                x[-1].append(xp)
                y[-1].append(yp)
                for u in bonds[i][k][z]:

                    if u[2] >= len(lattice[0][0]):
                        pass
                    else:
                        xb = (
                            lattice[u[0]][u[1]][u[2]][0] * unit_x[0]
                            + lattice[u[0]][u[1]][u[2]][1] * unit_y[0]
                        )
                        yb = (
                            lattice[u[0]][u[1]][u[2]][0] * unit_x[1]
                            + lattice[u[0]][u[1]][u[2]][1] * unit_y[1]
                        )

                        b[-1].append([[xp, yp], [xb, yb]])

    # first BL

    BL_num = 4

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(xlim=(min_x, max_x), ylim=(min_y, max_y))

    # Draw repeatition unit
    l1 = mlines.Line2D([0, unit_x[0] * nl], [0, 0], c="black")
    l2 = mlines.Line2D([unit_x[0] * nl, max_x - 1], [0, max_y - 1], c="black")
    l3 = mlines.Line2D([max_x - 1, unit_y[0] * nl], [max_y - 1, max_y - 1], c="black")
    l4 = mlines.Line2D([unit_y[0] * nl, 0], [max_y - 1, 0], c="black")
    ax.add_line(l1)
    ax.add_line(l2)
    ax.add_line(l3)
    ax.add_line(l4)

    # draw bonding
    for d in b[BL_num * 2]:
        l = mlines.Line2D([d[0][0], d[1][0]], [d[0][1], d[1][1]])
        ax.add_line(l)

    for d in b[BL_num * 2 + 1]:
        l = mlines.Line2D([d[0][0], d[1][0]], [d[0][1], d[1][1]])
        ax.add_line(l)

    # draw atoms
    ax.scatter(x[BL_num * 2], y[BL_num * 2], c="b", s=30)
    ax.scatter(x[BL_num * 2 + 1], y[BL_num * 2 + 1], c="r", s=30)

    plt.show()


def deposition():
    # choose a position to deposit an atom
    global mod, atom_set, n_atoms, cov, max_layer

    # check nuber of atoms

    num_atom = 0
    for i in range(len(atom_set)):
        for k in range(len(atom_set[i])):
            for z in range(len(atom_set[i][k])):
                if atom_set[i][k][z] != 0:
                    num_atom += 1
    if num_atom != n_atoms:
        print("Mass error")
        print("deposited atom = " + str(n_atoms))
        print("caculated atom = " + str(num_atom))
    candidate = []
    mod = []
    n_atoms = n_atoms + 1
    cov = n_atoms / NBL
    if n_atoms in (5, 20, 300):
        show_current()

    if n_atoms >= max_atom:
        print("max_reached")

    # first bilayer (directlly attached to substrate) is always the candidate
    for i in range(len(lattice)):
        for k in range(len(lattice[i])):
            if atom_set[i][k][0] == 0:
                candidate.append([i, k, 0])
            if atom_set[i][k][1] == 0:
                candidate.append([i, k, 1])

    # the neighbor sites of existing atoms are candidates
    for i in range(len(atom_set)):
        for k in range(len(atom_set[i])):
            for z in range(len(atom_set[i][k])):
                if atom_set[i][k][z] == 0:
                    pass
                else:
                    for u in bonds[i][k][z]:
                        if atom_set[u[0]][u[1]][u[2]] == 0:
                            candidate.append([u[0], u[1], u[2]])
                        else:
                            pass

    # Delete duplication
    candidate2 = []
    for i in candidate:
        if (i in candidate2) == False:
            candidate2.append(i)

    # Choose a site
    r = random.random()
    num = math.floor(r * len(candidate2))
    dep = candidate2[num]

    # mod: Sites that should change the probability of events
    mod.append(dep)

    # Check the structure of surrounding atoms
    st = 2
    if dep[2] == maxz:
        print("atom at maxz")
    if dep[2] > max_layer:
        max_layer = dep[2]

    for u in bonds[dep[0]][dep[1]][dep[2]]:
        # if at leat one atom around the deposition site is 3D, deposit atom is also 3D.
        if atom_set[u[0]][u[1]][u[2]] == 3:
            st = 3
            mod.append(u)
        elif atom_set[u[0]][u[1]][u[2]] == 2:
            mod.append(u)

    atom_set[dep[0]][dep[1]][dep[2]] = st


def params():
    global pre, Eagsi, E12, E23, E34, E45, E56, Eintra, Einter, Eagtp, Etr, Vene, rec, rec1
    global d_rate, NBL
    pre = float(entry_pre.get())
    Eagsi = float(entry_AgSi.get())
    E12 = float(entry_Si12.get())
    E23 = float(entry_Si23.get())
    E34 = float(entry_Si34.get())
    E45 = float(entry_Si45.get())
    E56 = float(entry_Si56.get())
    Eintra = float(entry_Siel.get())
    Einter = float(entry_Sielin.get())
    Eagtp = float(entry_Agtp.get())
    Etr = float(entry_tr.get())

    Vene = [E12, E23, E34, E45, E56, Eintra, Einter]
    rec = float(entry_img.get())
    rec1 = float(entry_img.get())

    # calculate deposition speed
    d_rate = float(entry_rate.get())  # ML/min
    d_rate = d_rate / 60  # ML/s
    NBL = 2 * nl * nl  # atoms/ML
    d_rate = d_rate * NBL  # atoms/s

    global ttime, dep_time
    dep_time = float(entry_time.get()) * 60
    post_time = float(entry_post.get()) * 60
    ttime = dep_time + post_time


def update_progress():
    text_time_c["text"] = str("{:.1f}".format(rel_time)) + " s"
    pbval = int(rel_time / ttime * 100)
    pb.configure(value=pbval)
    text_count["text"] = str(pbval) + " %"
    text_event["text"] = str(event_num) + " events"
    text_coverage["text"] = str("{:.2f}".format(cov)) + " ML"
    text_atoms["text"] = str("{:.2f}".format(n_atoms)) + " atoms"
    root.update()


def time_progress():
    global rel_time, tot, pbval, rec, rec1
    r2 = 0
    while r2 == 0:
        r2 = random.random()
    ratio = int(rel_time / ttime * 100)
    dt = -math.log(r2) / tot
    rel_time = rel_time + dt
    # recording
    if ratio >= rec:
        rec_atoms()
        rec = rec + rec1


def rec_atoms():
    global a_set_rec, cov_rec, t_rec, cov
    a_set_rec.append([])

    a_set_rec[-1] = copy.deepcopy(atom_set)

    cov_rec.append(cov)
    t_rec.append(rel_time)


def cal_rate(E):
    global kbt, pre
    rate = pre * math.exp(E / kbt)
    return rate


def update_events():
    global mod, event, event_time, event_tot, tot
    # Modify the event at the site in mod
    for e in mod:
        i = e[0]
        k = e[1]
        z = e[2]
        tot = tot - event_tot[i][k][z]
        event[i][k][z] = []
        event_time[i][k][z] = []
        event_tot[i][k][z] = 0
        tot_rec = 0
        # 最初はシンプルに組んで後で考え直す
        if atom_set[i][k][z] == 0:
            pass
        elif z == 0:
            # calculate total energy
            E = Eagsi
            for u in bonds[i][k][z]:
                s = atom_set[u[0]][u[1]][u[2]]
                if s != 0:
                    E += E12
            # get rate constant
            kr = cal_rate(E)
            # Record possible events and rate
            for u in bonds[i][k][z]:
                if atom_set[u[0]][u[1]][u[2]] == 0:
                    # empty neighbor site
                    event[i][k][z].append(["m", u[0], u[1], u[2]])
                    event_time[i][k][z].append(kr)
                    tot_rec += kr
                else:
                    # filled neighbor site
                    # Jucge upclimb event
                    sx = u[0]
                    sy = u[1]
                    sz = u[2] + 1
                    if atom_set[sx][sy][sz] == 0:
                        # upclimb possible
                        event[i][k][z].append(["u", sx, sy, sz])
                        event_time[i][k][z].append(kr)
                        tot_rec += kr
                    else:
                        # upclimb impossible
                        pass
        elif z == 1:
            # calculate total energy
            E = Eagsi
            for u in bonds[i][k][z]:
                s = atom_set[u[0]][u[1]][u[2]]
                if (s != 0) and (u[2] == 1):
                    # bonding with 0th atoms
                    E += E12
                elif (s != 0) and (u[2] == 3):
                    # bonding with next bilayer
                    E += E23
            # get rate constant
            kr = cal_rate(E)
            # Record possible events and rate
            for u in bonds[i][k][z]:
                if (atom_set[u[0]][u[1]][u[2]] == 0) and (u[2] == 0):
                    # empty neighbor site
                    event[i][k][z].append(["m", u[0], u[1], u[2]])
                    event_time[i][k][z].append(kr)
                    tot_rec += kr
                else:
                    pass
        elif (z == 2) or (z == 4):
            # calculate total energy
            E = 0
            for u in bonds[i][k][z]:
                s = atom_set[u[0]][u[1]][u[2]]
                if (s != 0) and (u[2] == z - 1):
                    # bonding with under BL
                    E += Vene[u[2]]
                elif (s != 0) and (u[2] == z + 1):
                    # bonding in same BL
                    E += Vene[u[2] + 1]
            # get rate constant
            kr = cal_rate(E)
            # Record possible events and rates
            for u in bonds[i][k][z]:
                if (atom_set[u[0]][u[1]][u[2]] == 0) and (u[2] == z + 1):
                    # empty neighbor site in same BL
                    event[i][k][z].append(["m", u[0], u[1], u[2]])
                    event_time[i][k][z].append(kr)
                    tot_rec += kr
                elif (atom_set[u[0]][u[1]][u[2]] == 0) and (u[2] == z - 1):
                    # empty neighbor site in lower BL
                    # Judge neighbor in lower site
                    judge = 0
                    for j in bonds[u[0]][u[1]][u[2]]:
                        if atom_set[j[0]][j[1]][j[2]] != 0:
                            judge += 1

                    if judge >= 2:
                        # the site has neighbor, which can make a bond. Candidate.
                        event[i][k][z].append(["m", u[0], u[1], u[2]])
                        event_time[i][k][z].append(kr)
                        tot_rec += kr
                elif (atom_set[u[0]][u[1]][u[2]] == 1) and (u[2] == z - 1):
                    # Downstair
                    for j in bonds[u[0]][u[1]][u[2]]:
                        if atom_set[j[0]][j[1]][j[2]] == 0:
                            # down stair possible
                            event[i][k][z].append(["d", j[0], j[1], j[2]])
                            event_time[i][k][z].append(kr)
                            tot_rec += kr
                        else:
                            pass
                elif (atom_set[u[0]][u[1]][u[2]] == 1) and (u[2] == z + 1):
                    # upstair
                    judge = 0
                    for j in bonds[u[0]][u[1]][[2]]:
                        if atom_set[j[0]][j[1]][j[2]] != 0:
                            judge += 1
                        else:
                            pass
                    if (judge >= 2) and (atom_set[u[0]][u[1]][u[2] + 1] == 0):
                        # upstair possible
                        event[i][k][z].append(["u", u[0], u[1], u[2] + 1])
                        event_time[i][k][z].append(kr)
                        tot_rec += kr
        elif z % 2 == 0:
            # calculate total energy
            E = 0
            for u in bonds[i][k][z]:
                s = atom_set[u[0]][u[1]][u[2]]
                if (s != 0) and (u[2] == z - 1):
                    # bonding with under BL
                    E += Vene[5]
                elif (s != 0) and (u[2] == z + 1):
                    # bonding in same BL
                    E += Vene[6]
            # get rate constant
            kr = cal_rate(E)
            # Record possible events and rates
            for u in bonds[i][k][z]:
                if (atom_set[u[0]][u[1]][u[2]] == 0) and (u[2] == z + 1):
                    # empty neighbor site in same BL
                    event[i][k][z].append(["m", u[0], u[1], u[2]])
                    event_time[i][k][z].append(kr)
                    tot_rec += kr
                elif (atom_set[u[0]][u[1]][u[2]] == 0) and (u[2] == z - 1):
                    # empty neighbor site in lower BL
                    # Judge neighbor in lower site
                    judge = 0
                    for j in bonds[u[0]][u[1]][u[2]]:
                        if atom_set[j[0]][j[1]][j[2]] != 0:
                            judge += 1

                    if judge >= 2:
                        # the site has neighbor, which can make a bond. Candidate.
                        event[i][k][z].append(["m", u[0], u[1], u[2]])
                        event_time[i][k][z].append(kr)
                        tot_rec += kr
                elif (atom_set[u[0]][u[1]][u[2]] == 1) and (u[2] == z - 1):
                    # Downstair
                    for j in bonds[u[0]][u[1]][u[2]]:
                        if atom_set[j[0]][j[1]][j[2]] == 0:
                            # down stair possible
                            event[i][k][z].append(["d", j[0], j[1], j[2]])
                            event_time[i][k][z].append(kr)
                            tot_rec += kr
                        else:
                            pass
                elif (atom_set[u[0]][u[1]][u[2]] == 1) and (u[2] == z + 1):
                    # upstair
                    judge = 0
                    for j in bonds[u[0]][u[1]][[2]]:
                        if atom_set[j[0]][j[1]][j[2]] != 0:
                            judge += 1
                        else:
                            pass

                    if (judge >= 2) and (atom_set[u[0]][u[1]][u[2] + 1] == 0):
                        # upstair possible
                        if u[2] + 1 >= maxz:
                            print("maxz reached")
                        event[i][k][z].append(["u", u[0], u[1], u[2] + 1])
                        event_time[i][k][z].append(kr)
                        tot_rec += kr

        elif (z == 3) or (z == 5):
            # calculate total energy
            E = 0
            for u in bonds[i][k][z]:
                s = atom_set[u[0]][u[1]][u[2]]
                if (s != 0) and (u[2] == z - 1):
                    # bonding in same BL
                    E += Vene[z]
                elif (s != 0) and (u[2] == z + 1):
                    # bonding with next bilayer
                    E += Vene[z + 1]
            # get rate constant
            kr = cal_rate(E)

            # Record possible events and rate
            for u in bonds[i][k][z]:
                if atom_set[u[0]][u[1]][u[2]] == 0:
                    # empty neighbor site
                    judge = 0
                    for j in bonds[u[0]][u[1]][u[2]]:
                        if atom_set[j[0]][j[1]][j[2]] != 0:
                            judge += 1

                    if judge >= 2:
                        # candidate
                        event[i][k][z].append(["m", u[0], u[1], u[2]])
                        event_time[i][k][z].append(kr)
                        tot_rec += kr

                else:
                    pass

        elif z % 2 == 1:
            # calculate total energy
            E = 0
            for u in bonds[i][k][z]:
                s = atom_set[u[0]][u[1]][u[2]]
                if (s != 0) and (u[2] == z - 1):
                    # bonding in same BL
                    E += Vene[6]
                elif (s != 0) and (u[2] == z + 1):
                    # bonding with next bilayer
                    E += Vene[5]
            # get rate constant
            kr = cal_rate(E)

            # Record possible events and rate
            for u in bonds[i][k][z]:
                if u[2] >= maxz:
                    print("maxz reached")
                elif atom_set[u[0]][u[1]][u[2]] == 0:
                    # empty neighbor site
                    judge = 0
                    for j in bonds[u[0]][u[1]][u[2]]:
                        if atom_set[j[0]][j[1]][j[2]] != 0:
                            judge += 1

                    if judge >= 2:
                        # candidate
                        event[i][k][z].append(["m", u[0], u[1], u[2]])
                        event_time[i][k][z].append(kr)
                        tot_rec += kr
                else:
                    pass

        else:
            print("No updates")
        event_tot[i][k][z] = tot_rec
        tot = tot + tot_rec

    mod = []


def event_progress(i, k, z, j):
    global atom_set, mod, max_layer

    if (
        (i >= len(event))
        or (k >= len(event[i]))
        or (z >= len(event[i][k]))
        or (j >= len(event[i][k][z]))
    ):
        print("Over")
        print("i = " + str(i))
        print("len(i) = " + str(len(event)))
        print("k = " + str(k))
        print("len(k) = " + str(len(event[i])))
        print("z = " + str(z))
        print("len(z) = " + str(len(event[i][k])))
        print("j = " + str(j))
        print("len(j) = " + str(len(event[i][k][z])))
        print("atomset = " + str(atom_set[i][k][z]))
        print("time = " + str(event_tot[i][k][z]))

    s = event[i][k][z][j]
    mod = []
    if atom_set[i][k][z] == 0:
        print("some mistake")

    if s[0] == "m":
        atom_set[i][k][z] = 0
        atom_set[s[1]][s[2]][s[3]] = 2
    elif s[0] == "u":
        atom_set[i][k][z] = 0
        atom_set[s[1]][s[2]][s[3]] = 2
    elif s[0] == "d":
        atom_set[i][k][z] = 0
        atom_set[s[1]][s[2]][s[3]] = 2
    elif s[0] == "t":
        pass
    if s[3] > max_layer:
        max_layer = s[3]

    mod.append([i, k, z])
    mod.append([s[1], s[2], s[3]])

    if bonds[i][k][z] == []:
        pass
    else:
        for a in bonds[i][k][z]:
            if atom_set[a[0]][a[1]][a[2]] != 0:
                mod.append([a[0], a[1], a[2]])

    if bonds[s[1]][s[2]][s[3]] == []:
        pass
    else:
        for a in bonds[s[1]][s[2]][s[3]]:
            if atom_set[a[0]][a[1]][a[2]] != 0:
                mod.append([a[0], a[1], a[2]])


def kMC():
    global tot, d_rate, rel_time, event_num
    event_num = 1
    while rel_time <= dep_time:
        update_progress()

        event_num = event_num + 1

        r1 = random.random()
        rt = r1 * tot
        # judge deposition
        if rt <= d_rate:
            # deposition happens
            deposition()
            # time progess
            time_progress()
            # update events and rates
            update_events()

        else:
            ie = 100
            rt = rt - d_rate
            for i in range(len(event_tot)):
                for k in range(len(event_tot[i])):
                    for z in range(len(event_tot[i][k])):
                        if rt <= 0:
                            pass
                        elif event_tot[i][k][z] == 0:
                            pass
                        elif rt <= event_tot[i][k][z]:
                            ie = i
                            ke = k
                            ze = z
                            trec = rt
                            rt = rt - event_tot[i][k][z]

                        else:
                            rt = rt - event_tot[i][k][z]

            if rt > 0:
                print("strange")
                print("tot = " + str(tot))
                print("remain = " + str(rt))
                print("ie =" + str(ie))
            else:
                for j in range(len(event_time[ie][ke][ze])):
                    # print(event_time[ie][ke][ze][j])
                    if trec <= 0:
                        pass
                    elif event_time[ie][ke][ze][j] == 0:
                        pass
                    elif trec <= event_time[ie][ke][ze][j]:
                        je = j
                        trec = trec - event_time[ie][ke][ze][j]
                    else:
                        trec = trec - event_time[ie][ke][ze][j]

                if trec > 0:
                    print("strange")
                    print("tot = " + str(tot))
                    print("remain = " + str(trec))

                else:

                    # event[ie][ke][ze][je] happens
                    event_progress(ie, ke, ze, je)
                    # time progess
                    time_progress()
                    # update events and rates
                    update_events()

    # deposition finish
    # post annealing
    tot = tot - d_rate

    # repetition untill post annealing finish
    while rel_time <= ttime:
        r1 = random.random()
        rt = r1 * tot

        for i in range(len(event_tot)):
            for k in range(len(event_tot[i])):
                for z in range(len(event_tot[i][k])):
                    if rt <= 0:
                        pass
                    elif event_tot[i][k][z] == 0:
                        pass
                    elif rt <= event_tot[i][k][z]:
                        ie = i
                        ke = k
                        ze = z
                        trec = rt
                        rt = rt - event_tot[i][k][z]
                    else:
                        rt = rt - event_tot[i][k][z]

        if rt > 0:
            print("strange")
            print("tot = " + str(tot))
            print("remain = " + str(rt))
            print("ie =" + str(ie))

        else:

            for j in range(len(event_time[ie][ke][ze])):
                if trec <= 0:
                    pass
                elif event_time[ie][ke][ze] == 0:
                    pass
                elif trec <= event_time[ie][ke][ze][j]:
                    je = j
                    trec = trec - event_time[ie][ke][ze][j]

            if trec > 0:
                pass
            else:
                # event[ie][ke][ze][je] happens
                event_progress(ie, ke, ze, je)
                # time progess
                time_progress()
                # update events and rates
                update_events()


def rec_pos():
    # record the position of atoms in poscar form
    for n in range(len(a_set_rec)):
        xp = []
        yp = []
        zp = []
        num = 0
        s = a_set_rec[n]

        for i in range(len(s)):
            for k in range(len(s[i])):
                for z in range(len(s[i][k])):
                    if s[i][k][z] != 0:
                        xp.append(lattice[i][k][z][0] / nl)
                        yp.append(lattice[i][k][z][1] / nl)
                        zp.append(lattice[i][k][z][2] / zl / 2.448)
                        num = num + 1

        file_name = (
            entry_rec.get() + "_" + str(int(t_rec[n])) + "s" + "_" + str(n) + ".vasp"
        )
        file_data = open(file_name, "w")
        file_data.write(entry_rec.get() + "\n")
        file_data.write("10" + "\n")

        file_data.write(str(nl) + "\t" + "0" + "\t" + "0" + "\n")
        file_data.write(str(nl / 2) + "\t" + str(nl / 2 * 1.732) + "\t" + "0" + "\n")
        file_data.write("0" + "\t" + "0" + "\t" + str(zl * 2.448) + "\n")
        file_data.write("Si" + "\n")
        file_data.write(str(num) + "\n")
        file_data.write("direct" + "\n")
        for i in range(len(xp)):
            file_data.write(str(xp[i]) + "\t" + str(yp[i]) + "\t" + str(zp[i]) + "\n")
        file_data.close()


def figure_draw_rec():
    for n in range(len(a_set_rec)):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        kx = figure_formation(ax, n)
        file_name = (
            entry_rec.get()
            + "_middle_"
            + str(int(t_rec[n]))
            + "s"
            + "_"
            + str(n)
            + ".png"
        )
        fig.savefig(file_name)
        images.append(file_name)


def coverage_color():
    global images, gray, green
    number = 0
    distribution = []
    for i in images:
        distribution.append([0, 0])
        number = number + 1
        img = Image.open(i)
        img.convert("RGB")
        psize = img.size
        for s in range(psize[0]):
            for t in range(psize[1]):
                r, g, b, no = img.getpixel((s, t))
                col = [r, g, b]

                if col == [128, 128, 128]:
                    distribution[-1][0] += 1
                elif col == [0, 255, 0]:
                    distribution[-1][1] += 1
    gray = []
    green = []
    for i in distribution:
        gray.append(i[0])
        green.append(i[1])


def hist_rec():
    global images_h
    images_h = []
    for k in range(len(layers_each)):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        kx = hist_formation(ax, k)

        file_name = (
            entry_rec.get()
            + "_hist_"
            + str(int(t_rec[k]))
            + "s"
            + "_"
            + str(k)
            + ".png"
        )
        fig.savefig(file_name)
        images_h.append(file_name)


def ppt_form():
    global images, images_h
    k = os.path.exists("Layer_analysis_results.pptx")
    if k == True:
        prs = Presentation("Layer_analysis_results.pptx")
    else:
        prs = Presentation()
        prs.slide_height = Inches(7.5)
        prs.slide_width = Inches(13.33)
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        title.text = "Layer analysis calculation results"
    # First page
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    width = height = Inches(1)
    top = Inches(0)
    left = Inches(0.5)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = "Parameters"
    p.font.size = Pt(28)
    shapes = slide.shapes
    left = Inches(0.5)
    top = Inches(1.5)
    rows = 2
    cols = 11
    width = Inches(12)
    height = Inches(1)
    # record parameters
    table0 = shapes.add_table(rows, cols, left, top, width, height).table
    table0.cell(0, 0).text = "Num. cells"
    table0.cell(0, 1).text = "Z units"
    table0.cell(0, 2).text = "T (K)"
    table0.cell(0, 3).text = "kbT"
    table0.cell(0, 4).text = "dep. rate (ML/min)"
    table0.cell(0, 5).text = "dep. time (min)"
    table0.cell(0, 6).text = "post anneal(min)"
    table0.cell(0, 7).text = "prefactor"
    table0.cell(0, 8).text = "transform"
    table0.cell(0, 9).text = "keep defect"
    table0.cell(0, 10).text = "Cal. time (s)"
    table0.cell(1, 0).text = str(nl)
    table0.cell(1, 1).text = str(zl)
    table0.cell(1, 2).text = entry_kbT.get()
    table0.cell(1, 3).text = str("{:.3g}".format(kbt))
    table0.cell(1, 4).text = entry_rate.get()
    table0.cell(1, 5).text = entry_time.get()
    table0.cell(1, 6).text = entry_post.get()
    table0.cell(1, 7).text = entry_pre.get()
    if bln_tr.get() == True:
        table0.cell(1, 8).text = "on"
    else:
        table0.cell(1, 8).text = "off"
    if bln_def.get() == True:
        table0.cell(1, 9).text = "on"
    else:
        table0.cell(1, 9).text = "off"
    table0.cell(1, 10).text = str(minute) + " m " + str(second) + " s"
    left = Inches(0.5)
    top = Inches(3.5)
    rows = 2
    cols = 11
    width = Inches(12)
    height = Inches(1)
    table = shapes.add_table(rows, cols, left, top, width, height).table
    table.cell(0, 1).text = "Ag-Si"
    table.cell(0, 2).text = "Si(1-2)"
    table.cell(0, 3).text = "Si(2-3)"
    table.cell(0, 4).text = "Si(3-4)"
    table.cell(0, 5).text = "Si(4-5)"
    table.cell(0, 6).text = "Si(5-6)"
    table.cell(0, 7).text = "Si(intra)"
    table.cell(0, 8).text = "Si(inter)"
    table.cell(0, 9).text = "Ag(top)"
    table.cell(0, 10).text = "Trans."
    table.cell(1, 0).text = "Energy"
    table.cell(1, 1).text = entry_AgSi.get()
    table.cell(1, 2).text = entry_Si12.get()
    table.cell(1, 3).text = entry_Si23.get()
    table.cell(1, 4).text = entry_Si34.get()
    table.cell(1, 5).text = entry_Si45.get()
    table.cell(1, 6).text = entry_Si56.get()
    table.cell(1, 7).text = entry_Siel.get()
    table.cell(1, 8).text = entry_Sielin.get()
    table.cell(1, 9).text = entry_Agtp.get()
    table.cell(1, 10).text = entry_tr.get()
    """
    left = Inches(0.5)
    top = Inches(6.5)
    rows = 2
    cols = 3
    width = Inches(8)
    height = Inches(0.5)

    table = shapes.add_table(rows, cols, left, top, width, height).table
    table.cell(0, 0).text = "Total energy"
    table.cell(0, 1).text = "1 ML"
    table.cell(0, 2).text = "Final"

    table.cell(1, 0).text = str('{:.3g}'.format(E))
    table.cell(1, 1).text = str('{:.3g}'.format(ML_check))
    table.cell(1, 2).text = str('{:.3g}'.format(final_check))
    """

    width = height = Inches(1)
    top = Inches(6)
    left = Inches(0.5)

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame

    p = tf.add_paragraph()
    p.text = entry_text.get()
    p.font.size = Pt(20)

    # second slide
    slide = prs.slides.add_slide(blank_slide_layout)

    width = height = Inches(1)
    top = Inches(-0.1)
    left = Inches(0.5)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame

    p = tf.add_paragraph()
    p.text = "Results"
    p.font.size = Pt(28)

    # put images

    left0 = 0.2
    top0 = 0.7
    height = Inches(2.5)
    height_w = Inches(1)

    num_ims = len(images)
    imn = 0
    slides = 0

    fin = 0

    while fin == 0:
        slides = slides + 1
        if slides != 1:
            slide = prs.slides.add_slide(blank_slide_layout)

            width = height = Inches(1)
            top = Inches(-0.1)
            left = Inches(0.5)
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame

            p = tf.add_paragraph()
            p.text = "Results"
            p.font.size = Pt(28)

            left0 = 0.2
            top0 = 0.7
            height = Inches(2.5)
            height_w = Inches(1)

        for i in range(0, 3):
            for k in range(0, 4):
                if imn >= num_ims:
                    fin = 1
                else:
                    left = Inches(left0 + k * 3.2)
                    top = Inches(top0 + i * 2.1)
                    slide.shapes.add_picture(images[imn], left, top, height=height)

                    txBox = slide.shapes.add_textbox(
                        left, top - Inches(0.2), width, height_w
                    )
                    tf = txBox.text_frame

                    p = tf.add_paragraph()
                    p.text = (
                        str(int(t_rec[imn]))
                        + " s, "
                        + str("{:.2f}".format(cov_rec[imn]))
                        + " ML"
                    )
                    p.font.size = Pt(20)

                    imn = imn + 1
        if imn == num_ims:
            fin = 1

    # Third slide
    slide = prs.slides.add_slide(blank_slide_layout)

    width = height = Inches(1)
    top = Inches(-0.1)
    left = Inches(0.5)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame

    p = tf.add_paragraph()
    p.text = "Results: layer analysis"
    p.font.size = Pt(28)

    # put images

    left0 = 0.2
    top0 = 0.7
    height = Inches(2)
    height_w = Inches(1)

    num_ims = len(images_h)
    imn = 0
    slides = 0

    fin = 0

    while fin == 0:
        slides = slides + 1
        if slides != 1:
            slide = prs.slides.add_slide(blank_slide_layout)
            width = height = Inches(1)
            top = Inches(-0.1)
            left = Inches(0.5)
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            p = tf.add_paragraph()
            p.text = "Results: layer analysis"
            p.font.size = Pt(28)
            left0 = 0.2
            top0 = 0.7
            height = Inches(2)
            height_w = Inches(1)
        for i in range(0, 3):
            for k in range(0, 4):
                if imn >= num_ims:
                    fin = 1
                else:
                    left = Inches(left0 + k * 3.2)
                    top = Inches(top0 + i * 2.1)
                    slide.shapes.add_picture(
                        images_h[imn], left, top + Inches(0.2), height=height
                    )

                    txBox = slide.shapes.add_textbox(
                        left, top - Inches(0.2), width, height_w
                    )
                    tf = txBox.text_frame

                    p = tf.add_paragraph()
                    p.text = (
                        str(int(t_rec[imn]))
                        + " s, "
                        + str("{:.2f}".format(cov_rec[imn]))
                        + " ML"
                    )
                    p.font.size = Pt(20)

                    imn = imn + 1
        if imn == num_ims:
            fin = 1
    """
    slide = prs.slides.add_slide(blank_slide_layout)

    width = height = Inches(1)
    top = Inches(-0.1)
    left = Inches(0.5)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame

    p = tf.add_paragraph()
    p.text = "Results: Coverage dependence"
    p.font.size = Pt(28)

    height = Inches(5.5)
    top = Inches(1)
    left = Inches(0.7)

    file_name = entry_rec.get() + "_coverage" + ".png"

    slide.shapes.add_picture(file_name, left, top, height=height)
    """
    prs.save("Layer_analysis_results.pptx")


def layer_sum():
    global layers_each, max_layer
    layers_each = []
    max_layer = 0
    for s in range(len(a_set_rec)):
        layers_each.append([])
        co = a_set_rec[s]
        for z in range(len(co[0][0])):
            c_each = 0
            if z % 2 == 0:
                count = 0
            for i in range(len(co)):
                for k in range(len(co[i])):
                    if co[i][k][z] != 0:
                        count += 1
                        c_each += 1
            if z % 2 == 1:
                layers_each[-1].append(count)
            if (c_each != 0) and (z >= max_layer):
                max_layer = z


def figure_formation(ax, n):
    length = nl
    p = pat.Polygon(
        xy=[
            (0, 0),
            (unit_x[0] * length, unit_x[1] * length),
            ((unit_x[0] + unit_y[0]) * length, (unit_x[1] + unit_y[1]) * length),
            (unit_y[0] * length, unit_y[1] * length),
        ],
        fc=(0.5, 0.5, 0.5),
        ec=(0, 0, 0),
    )
    ax.add_patch(p)
    atom_set_n = a_set_rec[n]
    for z in range(0, max_layer):
        for i in range(len(atom_set_n)):
            for k in range(len(atom_set_n[i])):
                if atom_set_n[i][k][z] == 0:
                    pass
                else:
                    xp = lattice[i][k][z][0]
                    yp = lattice[i][k][z][1]
                    zp = lattice[i][k][z][2]
                    if z % 2 == 0:
                        t1x = (
                            xp * unit_x[0]
                            + yp * unit_y[0]
                            - (unit_x[0] + unit_y[0]) / 3
                        )
                        t1y = (
                            xp * unit_x[1]
                            + yp * unit_y[1]
                            - (unit_x[1] + unit_y[1]) / 3
                        )

                        t2x = t1x + unit_x[0]
                        t2y = t1y + unit_x[1]

                        t3x = t1x + unit_y[0]
                        t3y = t1y + unit_y[1]

                    else:
                        t1x = (
                            xp * unit_x[0]
                            + yp * unit_y[0]
                            + (unit_x[0] + unit_y[0]) / 3
                        )
                        t1y = (
                            xp * unit_x[1]
                            + yp * unit_y[1]
                            + (unit_x[1] + unit_y[1]) / 3
                        )

                        t2x = t1x - unit_x[0]
                        t2y = t1y - unit_x[1]

                        t3x = t1x - unit_y[0]
                        t3y = t1y - unit_y[1]

                    color_num = math.floor(z / 2) * 2
                    if z == 1 or z == 0:
                        color = [0, 1, 0]
                    else:
                        color = [color_num / max_layer, 0, 1 - color_num / max_layer]

                    p = pat.Polygon(
                        xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                    )

                    ax.add_patch(p)

                    if i == 0:
                        if z % 2 == 0:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                - (unit_x[0] + unit_y[0]) / 3
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                - (unit_x[1] + unit_y[1]) / 3
                                + unit_x[1] * length
                            )

                            t2x = t1x + unit_x[0]
                            t2y = t1y + unit_x[1]

                            t3x = t1x + unit_y[0]
                            t3y = t1y + unit_y[1]
                        else:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                + (unit_x[0] + unit_y[0]) / 3
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                + (unit_x[1] + unit_y[1]) / 3
                                + unit_x[1] * length
                            )

                            t2x = t1x - unit_x[0]
                            t2y = t1y - unit_x[1]

                            t3x = t1x - unit_y[0]
                            t3y = t1y - unit_y[1]

                        p = pat.Polygon(
                            xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                        )
                        ax.add_patch(p)

                    if k == 0:
                        if z % 2 == 0:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                - (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                - (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                            )

                            t2x = t1x + unit_x[0]
                            t2y = t1y + unit_x[1]

                            t3x = t1x + unit_y[0]
                            t3y = t1y + unit_y[1]
                        else:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                + (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                + (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                            )

                            t2x = t1x - unit_x[0]
                            t2y = t1y - unit_x[1]

                            t3x = t1x - unit_y[0]
                            t3y = t1y - unit_y[1]

                        p = pat.Polygon(
                            xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                        )
                        ax.add_patch(p)

                    if (i == 0) and (k == 0):

                        if z % 2 == 0:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                - (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                - (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                                + unit_x[1] * length
                            )

                            t2x = t1x + unit_x[0]
                            t2y = t1y + unit_x[1]

                            t3x = t1x + unit_y[0]
                            t3y = t1y + unit_y[1]
                        else:
                            t1x = (
                                xp * unit_x[0]
                                + yp * unit_y[0]
                                + (unit_x[0] + unit_y[0]) / 3
                                + unit_y[0] * length
                                + unit_x[0] * length
                            )
                            t1y = (
                                xp * unit_x[1]
                                + yp * unit_y[1]
                                + (unit_x[1] + unit_y[1]) / 3
                                + unit_y[1] * length
                                + unit_x[1] * length
                            )

                            t2x = t1x - unit_x[0]
                            t2y = t1y - unit_x[1]

                            t3x = t1x - unit_y[0]
                            t3y = t1y - unit_y[1]

                        p = pat.Polygon(
                            xy=[(t1x, t1y), (t2x, t2y), (t3x, t3y)], fc=color, ec=color
                        )
                        ax.add_patch(p)

    p = pat.Polygon(
        xy=[(0, 0), (unit_y[0] * length, unit_y[1] * length), (0, unit_y[1] * length)],
        fc=(1, 1, 1),
        ec=(0, 0, 0),
    )
    ax.add_patch(p)

    p = pat.Polygon(
        xy=[
            (unit_x[0] * length, 0),
            ((unit_x[0] + unit_y[0]) * length, 0),
            ((unit_x[0] + unit_y[0]) * length, (unit_x[1] + unit_y[1]) * length),
        ],
        fc=(1, 1, 1),
        ec=(0, 0, 0),
    )
    ax.add_patch(p)

    ax.set_xlim(0, (unit_x[0] + unit_y[0]) * length)
    ax.set_ylim(0, (unit_x[1] + unit_y[1]) * length)
    ax.set_aspect("equal")

    return ax


def hist_formation(bx, n):
    numbers = layers_each[n]
    lay = []
    for i in range(len(numbers)):
        lay.append(i + 1)

    left = np.arange(len(numbers))

    bx.barh(left, numbers)
    bx.set_yticks(left)
    bx.set_yticklabels(lay)
    bx.set_xlabel("Coverage")
    bx.set_ylabel("layer number")

    bx.set_xlim(0, NBL)
    return bx


def figure_draw(n):
    ax = fig.add_subplot(211)
    ax.cla()
    ax = fig.add_subplot(211)
    kx = figure_formation(ax, n)
    # hist
    bx = fig.add_subplot(212)
    bx.cla()
    bx = fig.add_subplot(212)
    jx = hist_formation(bx, n)


def show_pictures():
    global canvas, imnum, fig
    root_p = tkinter.Toplevel()
    root_p.geometry("650x630")

    def p1_clicked():
        global imnum, cov_rec, canvas, fig
        imnum = imnum - 1
        if imnum < 0:
            imnum = len(cov_rec) - 1
        figure_draw(imnum)
        canvas.draw()
        canvas.get_tk_widget().pack()
        text_p8["text"] = str(int(t_rec[imnum])) + " s"
        text_p4["text"] = str(cov_rec[imnum])
        text_p6["text"] = str(imnum + 1) + "/" + str(len(cov_rec))

    def p2_clicked():
        global imnum, cov_rec, canvas, fig
        imnum = imnum + 1
        if imnum >= len(cov_rec):
            imnum = 0
        figure_draw(imnum)
        canvas.draw()
        canvas.get_tk_widget().pack()
        text_p8["text"] = str(int(t_rec[imnum])) + " s"
        text_p4["text"] = str(cov_rec[imnum])
        text_p6["text"] = str(imnum + 1) + "/" + str(len(cov_rec))

    button_p1 = tkinter.Button(
        root_p, text="Previous", command=p1_clicked, height=2, width=25
    )
    button_p1.place(x=30, y=560)
    button_p2 = tkinter.Button(
        root_p, text="Next", command=p2_clicked, height=2, width=25
    )
    button_p2.place(x=230, y=560)
    text_p7 = tkinter.Label(root_p, text="Time: ", font=("", 16))
    text_p7.place(x=30, y=500)
    text_p8 = tkinter.Label(root_p, text=str(cov_rec[0]), font=("", 16))
    text_p8.place(x=130, y=500)
    text_p3 = tkinter.Label(root_p, text="Coverage: ", font=("", 16))
    text_p3.place(x=230, y=500)
    text_p4 = tkinter.Label(root_p, text=str(cov_rec[0]), font=("", 16))
    text_p4.place(x=350, y=500)
    text_p6 = tkinter.Label(root_p, text="1/" + str(len(cov_rec)), font=("", 16))
    text_p6.place(x=450, y=500)
    imnum = len(cov_rec) - 1
    fig = plt.Figure()
    text_p8["text"] = str(int(t_rec[imnum])) + " s"
    text_p4["text"] = str(cov_rec[imnum])
    text_p6["text"] = str(imnum + 1) + "/" + str(len(cov_rec))
    figure_draw(imnum)
    canvas = FigureCanvasTkAgg(fig, master=root_p)
    canvas.draw()
    canvas.get_tk_widget().pack()

    def button_closep_clicked():
        plt.close("all")
        root_p.destroy()

    button_closep = tkinter.Button(
        root_p, text="Close", command=button_closep_clicked, height=2, width=25
    )
    button_closep.place(x=430, y=560)
    root_p.mainloop()


def cal_start():
    global lattice, atom_set, bonds, event, mod, rel_time, tot
    global a_set_rec, cov_rec, t_rec, images, d_rate
    start = time.time()
    pbval = 0
    pb.configure(value=pbval)
    text_count["text"] = "Started"
    text_coverage["text"] = "0 ML"
    root.update()
    # lists for recording
    a_set_rec = []
    cov_rec = []
    t_rec = []
    images = []
    # form lattice
    lattice_form()
    params()
    # tot: sum of rate constants. First, only deposition
    tot = d_rate
    # evaporation start
    rel_time = 0
    # first deposition
    global n_atoms
    n_atoms = 0
    deposition()
    text_count["text"] = "0 %"
    root.update()
    time_progress()
    # record first deposition
    rec_atoms()
    # update events and rates
    update_events()
    # second atomdepsoition
    deposition()
    time_progress()
    update_events()
    # repetition
    kMC()
    # record final structure
    text_count["text"] = "Saving"
    rec_atoms()
    # make poscar
    rec_pos()
    # record figures
    layer_sum()
    figure_draw_rec()
    coverage_color()
    hist_rec()
    global minute, second
    elapsed_time = time.time() - start
    minute = math.floor(elapsed_time / 60)
    second = int(elapsed_time % 60)
    text_count["text"] = str(minute) + " min " + str(second) + " sec"
    text_count["text"] = "PPT forming"
    ppt_form()
    text_count["text"] = "Finished"
    root.update()
    # calculation end
    # Show results
    show_pictures()


def button_start_clicked():
    # lattice_form_check()
    cal_start()


def button_close_clicked():
    plt.close("all")
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("kMC_Si_ver1")
    root.geometry("800x550")
    global unit_x, unit_y, unit_z, ims, max_layer
    unit_x: List[float] = [1, 0, 0]
    unit_y: List[float] = [0.5, 0.866, 0]
    unit_z: List[float] = [0, 0, 1]
    zd1 = 0.204
    zd2 = 0.612
    max_layer = 0
    global c_num
    c_num = 0

    arx: List[int] = [0, 20, 140, 200, 300, 380, 500, 560, 660]
    ary: List[int] = [0, 20, 50, 100, 130, 160, 0, 190, 220, 250, 280, 310]
    #
    entry_1 = tkinter.Entry(root, text="Number of cell", width=7)
    entry_1.place(x=arx[2], y=ary[1])
    text_1 = tkinter.Label(root, text="Number of cell")
    text_1.place(x=arx[1], y=ary[1])
    entry_1.delete(0, tkinter.END)
    entry_1.insert(tkinter.END, "5")
    entry_1.bind("<Return>", update)
    #
    entry_zunit = tkinter.Entry(root, text="Z unit", width=7)
    entry_zunit.place(x=arx[4], y=ary[1])
    text_zunit = tkinter.Label(root, text="Z unit")
    text_zunit.place(x=arx[3], y=ary[1])
    entry_zunit.delete(0, tkinter.END)
    entry_zunit.insert(tkinter.END, "5")
    entry_zunit.bind("<Return>", update)
    #
    entry_kbT = tkinter.Entry(root, text="T (K)", width=7)
    entry_kbT.place(x=arx[6], y=ary[1])
    text_kbT = tkinter.Label(root, text="T (K)")
    text_kbT.place(x=arx[5], y=ary[1])
    entry_kbT.delete(0, tkinter.END)
    entry_kbT.insert(tkinter.END, "550")
    entry_kbT.bind("<Return>", update)
    #
    global kbt
    kbt = float(entry_kbT.get()) * 8.617e-5
    #
    text_lkbt = tkinter.Label(root, text="kbT")
    text_lkbt.place(x=arx[7], y=ary[1])
    text_kbt = tkinter.Label(root, text=str("{:.3g}".format(kbt)))
    text_kbt.place(x=arx[8], y=ary[1])

    entry_rate = tkinter.Entry(root, text="dep_rate", width=7)
    entry_rate.place(x=arx[2], y=ary[2])
    text_2 = tkinter.Label(root, text="dep_rate (ML/min)")
    text_2.place(x=arx[1], y=ary[2])
    entry_rate.delete(0, tkinter.END)
    entry_rate.insert(tkinter.END, "0.4")
    entry_rate.bind("<Return>", update)

    text_ats = tkinter.Label(root, text="0")
    text_ats.place(x=arx[2], y=ary[2] + 30)

    entry_time = tkinter.Entry(root, text="Dep.time", width=7)
    entry_time.place(x=arx[4], y=ary[2])
    text_time = tkinter.Label(root, text="Dep.time (min)")
    text_time.place(x=arx[3], y=ary[2])
    entry_time.delete(0, tkinter.END)
    entry_time.insert(tkinter.END, "5")
    entry_time.bind("<Return>", update)

    entry_post = tkinter.Entry(root, text="Post annealing", width=7)
    entry_post.place(x=arx[6], y=ary[2])
    text_post = tkinter.Label(root, text="Post anneal (min)")
    text_post.place(x=arx[5], y=ary[2])
    entry_post.delete(0, tkinter.END)
    entry_post.insert(tkinter.END, "0")

    entry_pre = tkinter.Entry(root, text="Prefactor (1/s)", width=7)
    entry_pre.place(x=arx[8], y=ary[2])
    text_pre = tkinter.Label(root, text="prefactor (1/s)")
    text_pre.place(x=arx[7], y=ary[2])
    entry_pre.delete(0, tkinter.END)
    entry_pre.insert(tkinter.END, "1e+13")
    entry_pre.bind("<Return>", update)

    text_bonding = tkinter.Label(root, text="Energy")
    text_bonding.place(x=20, y=ary[4])

    # Ag-Si
    text_AgSi = tkinter.Label(root, text="Ag-Si")
    text_AgSi.place(x=100, y=ary[3])
    entry_AgSi = tkinter.Entry(root, text="Ag-Si", width=7)
    entry_AgSi.place(x=100, y=ary[4])
    entry_AgSi.delete(0, tkinter.END)
    entry_AgSi.insert(tkinter.END, "-1.4")
    entry_AgSi.bind("<Return>", update)
    # Si1-2
    text_Si12 = tkinter.Label(root, text="Si(1-2)")
    text_Si12.place(x=180, y=ary[3])
    entry_Si12 = tkinter.Entry(root, text="Si(1-2)", width=7)
    entry_Si12.place(x=180, y=ary[4])
    entry_Si12.delete(0, tkinter.END)
    entry_Si12.insert(tkinter.END, "-1.2")
    entry_Si12.bind("<Return>", update)
    # Si2-3
    text_Si23 = tkinter.Label(root, text="Si(2-3)")
    text_Si23.place(x=260, y=ary[3])
    entry_Si23 = tkinter.Entry(root, text="Si(2-3)", width=7)
    entry_Si23.place(x=260, y=ary[4])
    entry_Si23.delete(0, tkinter.END)
    entry_Si23.insert(tkinter.END, "-1.3")
    entry_Si23.bind("<Return>", update)
    # Si3-4
    text_Si34 = tkinter.Label(root, text="Si(3-4)")
    text_Si34.place(x=340, y=ary[3])
    entry_Si34 = tkinter.Entry(root, text="Si(3-4)", width=7)
    entry_Si34.place(x=340, y=ary[4])
    entry_Si34.delete(0, tkinter.END)
    entry_Si34.insert(tkinter.END, "-1.3")
    entry_Si34.bind("<Return>", update)
    # Si4-5
    text_Si45 = tkinter.Label(root, text="Si(4-5)")
    text_Si45.place(x=420, y=ary[3])
    entry_Si45 = tkinter.Entry(root, text="Si(4-5)", width=7)
    entry_Si45.place(x=420, y=ary[4])
    entry_Si45.delete(0, tkinter.END)
    entry_Si45.insert(tkinter.END, "-1.4")
    entry_Si45.bind("<Return>", update)
    # Si5-6
    text_Si56 = tkinter.Label(root, text="Si(5-6)")
    text_Si56.place(x=500, y=ary[3])
    entry_Si56 = tkinter.Entry(root, text="Si(5-6)", width=7)
    entry_Si56.place(x=500, y=ary[4])
    entry_Si56.delete(0, tkinter.END)
    entry_Si56.insert(tkinter.END, "-1.4")
    entry_Si56.bind("<Return>", update)
    # else between layers
    text_Siel = tkinter.Label(root, text="Si(intra)")
    text_Siel.place(x=580, y=ary[3])
    entry_Siel = tkinter.Entry(root, text="Si(intra)", width=7)
    entry_Siel.place(x=580, y=ary[4])
    entry_Siel.delete(0, tkinter.END)
    entry_Siel.insert(tkinter.END, "-1.4")
    entry_Siel.bind("<Return>", update)
    # else inter layers
    text_Sielin = tkinter.Label(root, text="Si(inter)")
    text_Sielin.place(x=660, y=ary[3])
    entry_Sielin = tkinter.Entry(root, text="Si(inter)", width=7)
    entry_Sielin.place(x=660, y=ary[4])
    entry_Sielin.delete(0, tkinter.END)
    entry_Sielin.insert(tkinter.END, "-1.4")
    entry_Sielin.bind("<Return>", update)
    # Agtop
    text_Agtp = tkinter.Label(root, text="Ag(top)")
    text_Agtp.place(x=740, y=ary[3])
    entry_Agtp = tkinter.Entry(root, text="Ag(top)", width=7)
    entry_Agtp.place(x=740, y=ary[4])
    entry_Agtp.delete(0, tkinter.END)
    entry_Agtp.insert(tkinter.END, "-0.65")
    entry_Agtp.bind("<Return>", update)
    # Reference rates
    text_rates = tkinter.Label(root, text="Rates/bond")
    text_rates.place(x=20, y=ary[5])
    # Ag-Si
    text_AgSi_rates = tkinter.Label(root, text="Rates/bond")
    text_AgSi_rates.place(x=100, y=ary[5])
    # Si1-2
    text_Si12_rates = tkinter.Label(root, text="Rates/bond")
    text_Si12_rates.place(x=180, y=ary[5])
    # Si2-3
    text_Si23_rates = tkinter.Label(root, text="Rates/bond")
    text_Si23_rates.place(x=260, y=ary[5])
    # Si3-4
    text_Si34_rates = tkinter.Label(root, text="Rates/bond")
    text_Si34_rates.place(x=340, y=ary[5])
    # Si4-5
    text_Si45_rates = tkinter.Label(root, text="Rates/bond")
    text_Si45_rates.place(x=420, y=ary[5])
    # Si5-6
    text_Si56_rates = tkinter.Label(root, text="Rates/bond")
    text_Si56_rates.place(x=500, y=ary[5])
    # else between layers
    text_Siel_rates = tkinter.Label(root, text="Rates/bond")
    text_Siel_rates.place(x=580, y=ary[5])
    # else inter layers
    text_Sielin_rates = tkinter.Label(root, text="Rates/bond")
    text_Sielin_rates.place(x=660, y=ary[5])
    # Agtop
    text_Agtp_rates = tkinter.Label(root, text="Rates/bond")
    text_Agtp_rates.place(x=740, y=ary[5])
    bln_tr = tkinter.BooleanVar()
    bln_tr.set(True)
    chk_tr = tkinter.Checkbutton(root, variable=bln_tr, text="Transformation")
    chk_tr.place(x=20, y=ary[7])
    entry_tr = tkinter.Entry(root, text="transformation", width=7)
    entry_tr.place(x=200, y=ary[7] + 5)
    entry_tr.delete(0, tkinter.END)
    entry_tr.insert(tkinter.END, "-0.3")
    entry_tr.bind("<Return>", update)
    bln_def = tkinter.BooleanVar()
    bln_def.set(True)
    chk_def = tkinter.Checkbutton(
        root, variable=bln_def, text="Keep defect in first layer"
    )
    chk_def.place(x=20, y=ary[8])
    text_rec = tkinter.Label(root, text="Record")
    text_rec.place(x=20, y=ary[9])
    entry_rec = tkinter.Entry(root, text="Name", width=50)
    entry_rec.place(x=100, y=ary[9])
    entry_rec.delete(0, tkinter.END)
    entry_rec.insert(tkinter.END, "kMC_rec")
    text_img = tkinter.Label(root, text="Image rec. (%) :  ")
    text_img.place(x=450, y=ary[9])
    entry_img = tkinter.Entry(root, text="img", width=10)
    entry_img.place(x=570, y=ary[9])
    entry_img.delete(0, tkinter.END)
    entry_img.insert(tkinter.END, "10")
    text_comment = tkinter.Label(root, text="Comments")
    text_comment.place(x=20, y=ary[10])
    entry_text = tkinter.Entry(root, text="Comments", width=110)
    entry_text.place(x=100, y=ary[10])
    entry_text.delete(0, tkinter.END)
    entry_text.insert(tkinter.END, "No comments")

    global pbval
    pbval = 0

    pb = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=350, mode="determinate")
    pb.configure(maximum=100, value=pbval)
    pb.place(x=350, y=ary[11] + 5)

    text_count = tkinter.Label(root, text="Waiting")
    text_count.place(x=720, y=ary[11] + 5)

    text_time_c = tkinter.Label(root, text="time (s)")
    text_time_c.place(x=370, y=ary[11] + 35)

    text_event = tkinter.Label(root, text="events")
    text_event.place(x=470, y=ary[11] + 35)

    text_atoms = tkinter.Label(root, text="Num. atoms")
    text_atoms.place(x=570, y=ary[11] + 35)

    text_coverage = tkinter.Label(root, text="Coverage")
    text_coverage.place(x=670, y=ary[11] + 35)
    button_start = tkinter.Button(
        root, text="Start", command=button_start_clicked, height=1, width=20
    )
    button_start.place(x=20, y=ary[11])
    button_close = tkinter.Button(
        root, text="Close", command=button_close_clicked, height=1, width=20
    )
    button_close.place(x=180, y=ary[11])
    update_values()
    root.mainloop()
