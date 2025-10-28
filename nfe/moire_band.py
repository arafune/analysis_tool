"""Module for calculating energy bands and potentials in a 2D hexagonal lattice."""

import numpy as np
from numpy.typing import NDArray

HARTREE = 3.67493260e-5  # 1 meV in Hartree units
EV = 27.21138602  # 1 eV in Hartree units
A = 46.036  # lattice constnat of Gr/Ir(111) in Bohr units
INV_ANG = 1.88972613  # Used to convert fro 1/Bohr


def energies(
    kx: NDArray[np.float64] | float,
    ky: NDArray[np.float64] | float,
    alpha_meV: float,
    beta_meV: float,
    lattice_const_bohr: float = A,
    mass: float = 1,
    *,
    verbose: bool = False,
) -> NDArray[np.float64]:
    """Calculate the energy bands for a 2D hexagonal moiré lattice.

    Parameters
    ----------
    kx : NDArray[np.float64] or float
        The kx component(s) of the wavevector(s).
    ky : NDArray[np.float64] or float
        The ky component(s) of the wavevector(s).
    alpha_meV : float
        The real part of the potential in meV.
    beta_meV : float
        The imaginary part of the potential in meV.
    lattice_const_bohr : float, optional
        Lattice constant in Bohr units (default: a).
    mass : float, optional
        Effective mass (default: 1).
    verbose : bool, optional
        If True, print debug information (default: False).

    Returns
    -------
    NDArray[np.float64]
        Array of sorted energy eigenvalues (in eV) for each (kx, ky).
        The shape is (..., 3), matching the broadcasted shape of kx and ky.

    """
    kx = np.array(kx)
    ky = np.array(ky)
    const_g = 4 * np.pi / (3 * lattice_const_bohr)
    rec_g1 = const_g * np.array([0, 0])
    rec_g2 = const_g * np.array([-3 / 2, np.sqrt(3) / 2])
    rec_g3 = const_g * np.array([-3 / 2, -np.sqrt(3) / 2])
    potential_v = (alpha_meV + 1j * beta_meV) * HARTREE

    kx, ky = np.broadcast_arrays(kx, ky)
    shape = np.broadcast(kx, ky).shape

    k_plus_g1 = np.stack([kx + rec_g1[0], ky + rec_g1[1]], axis=-1)
    k_plus_g2 = np.stack([kx + rec_g2[0], ky + rec_g2[1]], axis=-1)
    k_plus_g3 = np.stack([kx + rec_g3[0], ky + rec_g3[1]], axis=-1)

    norm_g1: NDArray[np.float64] = np.linalg.norm(k_plus_g1, axis=-1) ** 2 / (2 * mass)
    norm_g3: NDArray[np.float64] = np.linalg.norm(k_plus_g3, axis=-1) ** 2 / (2 * mass)
    norm_g2: NDArray[np.float64] = np.linalg.norm(k_plus_g2, axis=-1) ** 2 / (2 * mass)

    energies_all = np.empty(shape + (3,), dtype=np.float64)

    for idx in np.ndindex(shape):
        h = np.zeros((3, 3), dtype=np.complex128)
        h[0, 0] = norm_g1[idx]
        h[1, 1] = norm_g2[idx]
        h[2, 2] = norm_g3[idx]
        h[0, 1] = potential_v
        h[1, 2] = potential_v
        h[2, 0] = potential_v
        h[0, 2] = np.conj(potential_v)
        h[1, 0] = np.conj(potential_v)
        h[2, 1] = np.conj(potential_v)
        energies_all[idx] = np.sort(np.linalg.eigvalsh(h) * EV)

    return energies_all


def potential(
    x: NDArray[np.float64] | float,
    y: NDArray[np.float64] | float,
    alpha_meV: float = 7.5,
    beta_meV: float = 1.1,
) -> float | NDArray[np.float64]:
    """Calculate the real-space moiré potential at position (x, y).

    Parameters
    ----------
    x : NDArray[np.float64] or float
        x-coordinate(s) in units of the moiré lattice.
    y : NDArray[np.float64] or float
        y-coordinate(s) in units of the moiré lattice.
    alpha_meV : float, optional
        Real part of the potential amplitude in meV (default: 7.5).
    beta_meV : float, optional
        Imaginary part of the potential amplitude in meV (default: 1.1).

    Returns
    -------
    float or NDArray[np.float64]
        The value(s) of the moiré potential at the given position(s).

    """
    return 2 * alpha_meV * (
        np.cos(4 * np.pi * y / np.sqrt(3))
        + 2 * np.cos(2 * np.pi * x) * np.cos(2 * np.pi * y / np.sqrt(3))
    ) + 2 * beta_meV * (
        np.sin(4 * np.pi * y / np.sqrt(3))
        + 2 * np.cos(2 * np.pi * x) * np.sin(2 * np.pi * y / np.sqrt(3))
    )
