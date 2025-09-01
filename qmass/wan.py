"""Module for reading data of Qmass measurement."""

from logging import DEBUG, INFO, Formatter, StreamHandler, getLogger
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import polars as pl

if TYPE_CHECKING:
    from numpy.typing import NDArray

LOGLEVELS = (DEBUG, INFO)
LOGLEVEL = LOGLEVELS[1]
logger = getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
formatter = Formatter(fmt)
handler = StreamHandler()
handler.setLevel(LOGLEVEL)
logger.setLevel(LOGLEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


class WAN:
    """Class for Qmass data measured by Microvision Plus (WAN).

    Attributes:
        header : dict[str, str]
        mode_data : dict[str, float | tuple[float, float]]
        scan : list[list[float]]
        mass_numbers : NDArray[np.float64]
        partial_pressures : NDArray[np.float64]

    """

    def __init__(self, fhandle: str) -> None:
        """Initialize (File load)."""
        self.header: dict[str, str]
        self.mode_data: dict[str, float | tuple[float, float]]
        self.scan: pl.DataFrame
        self.header, self.mode_data, self.scan = self.loader(fhandle)
        assert isinstance(self.mode_data["MASS RANGE"], tuple)
        mass_end = self.mode_data["MASS RANGE"][1]
        physical_step = _determine_physical_step(
            int(self.mode_data["PEAK DATA LENGTH"]),
        )
        scan_start = float(
            mass_end + 0.5 - 255 * physical_step,
        )
        self.mass_numbers: NDArray[np.float64] = np.linspace(
            scan_start,
            mass_end + 0.5,
            256,
        )
        self.partial_pressures: NDArray[np.float64] = (
            self.scan.mean_horizontal().to_numpy()
        )

    def loader(
        self,
        fhandle: str | Path,
    ) -> tuple[
        dict[str, str],
        dict[str, float | tuple[float, float]],
        pl.DataFrame,
    ]:
        """Load data from file.

        Args:
            fhandle : (str | Path)

        Returns:
            tuple[
                dict[str, str],
                dict[str, float | tuple[float, float]],
                pl.DataFrame,
            ]:

        """
        file_handle = Path(fhandle)
        if not file_handle.exists():
            msg = f"{file_handle} is not found."
            raise FileNotFoundError(msg)
        with file_handle.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # Header
        header: dict[str, str] = {}
        mode_data: dict[str, float | bool | tuple[float, float]] = {}
        scan: list[list[float]] = []

        mode = "header"
        for _ in lines:
            line = _.strip()
            if line.startswith('"[MODE DATA]"'):
                mode = "mode_data"
                continue
            if line.startswith('"[SCAN DATA]"'):
                mode = "scan_data"
                continue

            if mode == "header":
                header.update(_header_parser(line))
            elif mode == "mode_data":
                mode_data.update(_mode_data_parser(line))
            elif mode == "scan_data":
                scan.append(_scan_data_parser(line))
            else:
                msg = "Cannot parse the file."
                raise ValueError(msg)

        return header, mode_data, pl.DataFrame(scan)


def _determine_physical_step(peak_data_length: int) -> float:
    """Determine physical step from peak data length."""
    physical_steps = {8: 0.25 / 8, 16: 0.25 / 4, 32: 0.25 / 2, 64: 0.25}
    return physical_steps.get(peak_data_length, _raise_value_error(peak_data_length))


def _raise_value_error(peak_data_length: int) -> None:
    """Raise ValueError for invalid peak data length."""
    msg = f"Invalid peak data length: {peak_data_length}"
    raise ValueError(msg)


def _scan_data_parser(line: str) -> list[float]:
    """Parse scan data line."""
    line_data = line.split(",")[7:-2]
    return [float(i) for i in line_data]


def _header_parser(line: str) -> dict[str, str]:
    """Parse header lines."""
    header: dict[str, str] = {}
    line_data = line.split(",")
    header[str(line_data[0][2:-2])] = str(line_data[1][2:-2])
    return header


def _mode_data_parser(line: str) -> dict[str, float | bool | tuple[float, float]]:
    """Parse mode data line."""
    mode_data: dict[str, float | bool | tuple[float, float]] = {}
    mode_line = line.split(",")
    key = mode_line[0][2:-2]
    logger.debug(f"key: {key}")
    if key.startswith("PEAK DATA LENGTH"):
        mode_data[key] = int(mode_line[1])
    elif key.startswith("SCAN RANGE"):
        mode_data[key] = (float(mode_line[1][1:-1]), float(mode_line[2][1:-1]))
    elif key.startswith(("AUTORANGE ENABLED", "TOTAL ENABLED")):
        if "OFF" in mode_line[1].upper():
            mode_data[key] = False
        elif "ON" in mode_line[1].upper():
            mode_data[key] = True
        else:
            msg = f"Cannot parse {line}"
            raise ValueError(msg)
    elif key.startswith("MASS RANGE"):
        mode_data[key] = (int(mode_line[1]), int(mode_line[2]))
    elif key.startswith("ACCURACY"):
        mode_data[key] = int(mode_line[1])
    else:
        msg = f"Cannot parse {line}"
        raise ValueError(msg)
    return mode_data
