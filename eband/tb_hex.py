#! /usr/bin/env python3
"""Band calculation for honeycomb 2D-lattice by tight binding model."""

import matplotlib.pyplot as plt
import numpy as np

a_size = 1000
#
k_vec_gm = np.zeros((2, a_size))
k_vec_mk = np.zeros((2, int(np.ceil(a_size / np.sqrt(3)))))
k_vec_kg = np.zeros((2, a_size))
#
lattice = 1.5
eps_en_1 = 4
eps_en_2 = 2
t = 1.0
#
k_vec_gm[0] = np.linspace(0, 2 * np.pi / (lattice * np.sqrt(3)), a_size)
k_vec_mk[0] = k_vec_gm[0][-1]
k_vec_mk[1] = np.linspace(
    0, 2 * np.pi / (lattice * 3.0), int(np.ceil(a_size / np.sqrt(3)))
)
k_vec_kg[0] = np.linspace(2 * np.pi / (lattice * np.sqrt(3)), 0, a_size)
k_vec_kg[1] = np.linspace(2 * np.pi / (lattice * 3), 0, a_size)


class Band:
    """Band structure

    Parameters
    -----------
    lattice: float, default=1.5
        lattice constant
    N: int, default=1000
        division number for k path.

    """

    def __init__(self, lattice=lattice, N=a_size):
        """Initialization."""
        self.lattice = lattice
        self.gm = np.zeros((2, N))
        self.mk = np.zeros((2, int(np.ceil(N / np.sqrt(3)))))
        self.kg = np.zeros((2, N))
        #
        self.gm[0] = np.linspace(0, 2 * np.pi / (lattice * np.sqrt(3)), N)
        self.mk[0] = self.gm[0][-1]
        self.mk[1] = np.linspace(
            0, 2 * np.pi / (lattice * 3.0), int(np.ceil(N / np.sqrt(3)))
        )
        self.kg[0] = np.linspace(2 * np.pi / (lattice * np.sqrt(3)), 0, N)
        self.kg[1] = np.linspace(2 * np.pi / (lattice * 3), 0, N)

    def energy(self, kx, ky, eps_1=eps_en_1, eps_2=eps_en_2, t=t):
        r"""Return the energy from the tight binding method.

        :math:`E(k_x, k_y) = \frac{\epsilon_1 + \epsilon_2}{2}
        \pm \sqrt{ \frac{(\epsilon_1 - \epsilon_2)^2}{4}
        + 4t^2 \left( \frac{1}{4} + \cos\left(\frac{\sqrt{3}k_x}{2} a \right)
        \cos\left(\frac{k_y}{2} a  \right)
        + \cos ^2\left( \frac{k_y}{2} a \right) \right)}`

        Parameters
        -----------
        kx: float, numpy.ndarray
            kx
        ky: float, numpy.ndarray
            ky
        eps_1: float, default 4
            Energy of the 1st kind of atom in the unit cell ('B' for example)
        eps_2: float, default 2
            Energy of the 2nd kind of atom in the unit cell ('N' for example)
        t: float, default 1
            Overlapping integral
        Returns
        --------
        tuple of two numpy.ndarray, tuple of two floats

        """
        root_part = np.sqrt(
            ((eps_1 - eps_2) ** 2) / 4.0
            + 4.0
            * t ** 2
            * (
                1 / 4
                + np.cos(kx * self.lattice * np.sqrt(3) / 2)
                * np.cos(ky * self.lattice / 2)
                + (np.cos(ky * self.lattice / 2)) ** 2
            )
        )
        return (eps_1 + eps_2) / 2 + root_part, (eps_1 + eps_2) / 2 - root_part


def distance(kdata):
    """Return the distace.

    Parameters
    ------------
    kdata: (2, D)-shape numpy.ndarray
        2D k-points data

    """
    dist = np.concatenate(
        (np.array([0.0]), np.cumsum(np.linalg.norm(np.diff(kdata), axis=0)))
    )
    return dist
