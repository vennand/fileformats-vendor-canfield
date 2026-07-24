import os
import logging
from pathlib import Path
import typing as ty
import pytest

# Set DEBUG logging for unittests

log_level = logging.WARNING

logger = logging.getLogger("fileformats")
logger.setLevel(log_level)

sch = logging.StreamHandler()
sch.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sch.setFormatter(formatter)
logger.addHandler(sch)

EXPORT_DIR_TEST_DATA_PATH = os.environ.get(
    "FILEFORMATS_VENDOR_CANFIELD_EXPORT_TEST_DATA"
)

skip_if_no_export_test_data = pytest.mark.skipif(
    not EXPORT_DIR_TEST_DATA_PATH,
    reason="FILEFORMATS_VENDOR_CANFIELD_EXPORT_TEST_DATA environment variable is not set",
)


# For debugging in IDE's don't catch raised exceptions and let the IDE
# break at it
if os.getenv("_PYTEST_RAISE", "0") != "0":

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call: pytest.CallInfo[ty.Any]) -> None:
        if call.excinfo is not None:
            raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo: pytest.ExceptionInfo[BaseException]) -> None:
        raise excinfo.value


def _cleansed_export_dirs() -> list[Path]:
    if not EXPORT_DIR_TEST_DATA_PATH:
        return []
    return [
        p
        for p in Path(EXPORT_DIR_TEST_DATA_PATH).iterdir()
        if not p.name.startswith(".") and p.is_dir()
    ]


@pytest.fixture(params=_cleansed_export_dirs(), ids=lambda p: p.name)
def cleansed_export_dir(request: pytest.FixtureRequest) -> Path:
    """Each cleansed export directory to test against, in turn"""
    return request.param  # type: ignore[no-any-return]
