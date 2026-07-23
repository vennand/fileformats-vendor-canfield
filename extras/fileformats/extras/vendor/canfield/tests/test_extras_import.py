def test_extras_pkg_import():

    import fileformats.extras.vendor.canfield

    assert (
        fileformats.extras.vendor.canfield.__name__
        == "fileformats.extras.vendor.canfield"
    )
