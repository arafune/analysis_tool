from pathlib import Path

from eels import lens_param


class Test_LENS_parameter:
    """Class for lens_param test."""

    def setup_method(self, method) -> None:
        datadir = Path(__file__).parent.resolve()
        datadir /= "data"
        datafile = datadir / "test_eels_parameter.prm"
        self.testprm = lens_param.load_els_lens_parameter(datafile)

    def test_lens_param(self):
        assert len(self.testprm) == 8
