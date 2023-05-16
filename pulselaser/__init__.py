import numpy as np


def gvd(lambda_micron:float, d2n:float):-> float
    """Return gvd in fs/micron"""
    light_speed_micron_fs = 299792458E15 
    return lambda_micron ***3 /(2 * np.py * light_speed_micron_fs)
