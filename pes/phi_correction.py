"""Function for phi correction."""

import numpy as np


def based_on_pes_130(energy: float) -> float:
    """Return the corrected phi value based on the energy."""
    best_values = {
        "a": np.float64(0.021659247779521107),
        "b": np.float64(-0.19962481847388602),
    }
    return best_values["a"] * energy + best_values["b"]
