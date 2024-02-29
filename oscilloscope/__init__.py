"""Module for oscilloscope data analysis."""

import numpy as np
from numpy.typing import NDArray

TIME_DURATION = 5e-10


def _reconstruct_time(
    time_array: NDArray[np.float64],
    amp_array: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Rearrange the time scale within the periodicity.  (Helpler function).

    [TODO:description]

    Parameters
    ----------
    time_array
        [TODO:description]
    amp_array
        [TODO:description]
    rep_ratio_Hz
        [TODO:description]

    Returns
    -------
    tuple[NDArray[np.float_], NDArray[np.float_]]
        [TODO:description]

    """
    index_ = np.count_nonzero(time_array < 0)
    time_duration = time_array[1] - time_array[0]
    while index_ != 0:
        try:
            time_array = np.linspace(
                time_array[index_],
                time_array[index_] + time_duration * (time_array.shape[0] - 1),
                time_array.shape[0],
            )
        except IndexError:
            time_array = np.linspace(
                time_array[-1] + time_duration,
                time_array[-1]
                + time_duration
                + time_duration * (time_array.shape[0] - 1),
                time_array.shape[0],
            )
        amp_array = np.roll(amp_array, shift=-index_)
        index_ = np.count_nonzero(time_array < 0)
    return time_array, amp_array


def rearrange_oscilloscope_data(
    oscilloscope_data: NDArray[np.float64],
    rep_ratio_Hz: float = 7.96025e7,  # noqa: N803
    time_duration: float = TIME_DURATION,
    *,
    sort: bool = False,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Rearrange oscilloscope data which can be assumed as the periodic signal.

    Parameters
    ----------
    oscilloscope_data: NDArray[np.float64]
        (N, 1) arrray
    rep_ratio_Hz: float
        Periodicity in Hz units.
    time_duration:
        time duration of the wave.  (Inverse of the sampling rate.)
    sort: bool
        if True, output data is sorted.

    Returns
    -------
    tuple[NDArray[np.float64], NDArray[np.float64]]
        Arranged wave data.

    """
    data_size = oscilloscope_data.shape[0]  # 25000 in our case
    time_data = np.linspace(0, time_duration * data_size, data_size)
    length_single_period = int(1 / rep_ratio_Hz / time_duration)  # 25 in our case.
    oscilloscope_data = oscilloscope_data.reshape((-1, length_single_period))
    time_offset = (
        int(1 / rep_ratio_Hz / time_duration) - 1 / rep_ratio_Hz / time_duration
    ) * time_duration  # -6.241952199993684e-11
    #
    time_data = time_data.reshape((-1, length_single_period))
    ref_time = time_data[0]
    #
    num_period = np.shape(time_data)[0]  # Usually 1000
    times = []
    amplitudes = []
    for i in range(num_period):
        time_corrected, amp_corrected = _reconstruct_time(
            ref_time + i * time_offset,
            oscilloscope_data[i],
        )
        times.append(time_corrected)
        amplitudes.append(amp_corrected)
    if sort:
        times_arr = np.array(times).ravel()
        amplitudes_arr = np.array(amplitudes).ravel()
        ind = np.argsort(times_arr)
        return np.sort(times_arr), np.take_along_axis(amplitudes_arr, ind, axis=-1)
    return np.array(times), np.array(amplitudes)
