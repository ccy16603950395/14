from saline_composite.materials import default_materials


def test_interface_degradation_rate_higher() -> None:
    mats = default_materials()
    assert mats["interface"].degradation_rate > mats["concrete"].degradation_rate
    assert mats["interface"].degradation_rate > mats["rock"].degradation_rate
