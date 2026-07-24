from pathlib import Path

from fileformats.vendor.canfield.medimage import ExportDir

from conftest import skip_if_no_export_test_data

pytestmark = skip_if_no_export_test_data


def test_export_dir_validation(cleansed_export_dir: Path) -> None:
    """Test that the ExportDir format is valid."""
    export_dir = ExportDir(cleansed_export_dir)
    deidentified = export_dir.deidentify()
    assert isinstance(deidentified, ExportDir)
