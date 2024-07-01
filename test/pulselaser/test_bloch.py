from pulselaser import bloch


def test_bloch_gaussian_envelope() -> None:
    """Test for bloch.gaussian_envelope."""
    assert bloch.gaussian_envelop(t=0.0, fwhm=10.0, intensity=1.0) == 1.0
    assert bloch.gaussian_envelop(t=40.0, fwhm=20.0, intensity=1.0, t0=50.0) == 0.5
    assert bloch.gaussian_envelop(t=50.0, fwhm=20.0, intensity=1.0, t0=50.0) == 1.0
    assert bloch.gaussian_envelop(t=60.0, fwhm=20.0, intensity=1.0, t0=50.0) == 0.5
