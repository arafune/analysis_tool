#!/usr/bin/env python3
"""Collection of Selmeier equation."""

import numpy as np


def air(lambda_micron):
    """Dispersion of Refractive index of air.

    https://refractiveindex.info/?shelf=other&book=air&page=Ciddor

    """
    return (
        1
        + 0.05792105 / (238.0185 - lambda_micron ** (-2))
        + 0.00167917 / (57.362 - lambda_micron ** (-2))
    )


def alphaBBO(lambda_micron):
    """Return reflactive index.

    http://www.newlightphotonics.com/Birefringent-Crystals/alpha-BBO-Crystals

    Return
    -------
        (n_o, n_e)
    """
    return (
        np.sqrt(
            2.67579
            + 0.02099 / (lambda_micron ** 2 - 0.00470)
            - 0.00528 * lambda_micron ** 2
        ),
        np.sqrt(
            2.31197
            + 0.01184 / (lambda_micron ** 2 - 0.01607)
            - 0.00400 * lambda_micron ** 2
        ),
    )


def quartz(lambda_micron):
    """Dispersion of refractive index of crystal quartz.

    Optics communications. 2011, vol. 284, issue 12, p. 2683-2686.
    """
    return (
        np.sqrt(
            1.28604141
            + 1.07044083
            * lambda_micron ** 2
            / (lambda_micron ** 2 - 1.00585997 * 1e-2)
            + 1.10202242 * lambda_micron ** 2 / (lambda_micron ** 2 - 100)
        ),
        np.sqrt(
            1.28851804
            + 1.09509924
            * lambda_micron ** 2
            / (lambda_micron ** 2 - 1.02101864 * 1e-2)
            + 1.15662475 * lambda_micron ** 2 / (lambda_micron ** 2 - 100)
        ),
    )
