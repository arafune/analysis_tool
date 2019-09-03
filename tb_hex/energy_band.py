#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

a_size = 1000
#
k_vec_gm = np.zeros((2, a_size))
k_vec_mk = np.zeros((2, int(a_size / np.ceil(a_size))))
k_vec_kg = np.zeros((2, a_size))
#
lattice = 1.4
#
k_vec_gm[0] = np.linspace(0, 2 * np.pi / (lattice * np.sqrt(3)), a_size)
k_vec_mk[0] = k_vec_gm[0][-1]
k_vec_mk[1] = np.linspace(0, 2 * np.pi / (lattice * 3.0),
                          np.ceil(a_size / np.sqrt(3)))
k_vec_kg[0] = np.linspace(2 * np.pi / (lattice * np.sqrt(3)), 0, a_size)
k_vec_kg[1] = np.linspace(2 * np.pi / (lattice * 3), 0, a_size)


def energy(kx, ky, eps_1=4, eps_2=2.1, t=1.0, lattice=1.4):
    """Return the energy from the tight binding method.

    Parameters
    -----------
    kx: numpy.ndarray
        kx, (2, D)-shape array
    ky: numpy.ndarray
        ky, (2, D)-shape array
    eps_1: float
        Energy of the 1st kind of atom in the unit cell ('B' for example)
    eps_2: float
        Energy of the 2nd kind of atom in the unit cell ('N' for example)
    t: float
        Overlapping integral
    lattice: float
        lattice constant

    Returns
    --------
        tuple of two numpy.ndarray

    """
    c = np.sqrt(((eps_1 - eps_2)**2) / 4.0 + 4.0 * t**2 *
                (1 / 4 + np.cos(kx * lattice * np.sqrt(3) / 2) *
                 np.cos(ky * lattice / 2) + (np.cos(ky * lattice / 2))**2))
    return (eps_1 + eps_2) / 2 + c, (eps_1 + eps_2) / 2 - c
