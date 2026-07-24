from fileformats.core import validated_property
from fileformats.core.exceptions import FormatMismatchError
from fileformats.generic import Directory
from fileformats.medimage import MedicalImagingData

from .lesion import LesionAnalysisDir, T2k
from .three_d import ThreeDCaptureDir


class ExportDir(Directory, MedicalImagingData):
    """Canfield data export directory: a session/patient-level export
    containing some combination of whole-body 3D captures, hand-held
    single-lesion captures and their Vectra/Dexi lesion analyses. The three
    aren't necessarily 1-1 (e.g. not every lesion capture has been analysed),
    so each sub-type is discovered independently rather than cross-referenced."""

    @validated_property
    def has_content(self) -> bool:
        if not (
            self.t2k_files or self.three_d_capture_dirs or self.lesion_analysis_dirs
        ):
            raise FormatMismatchError(
                "Did not find any T2k files or ThreeDCaptureDir/LesionAnalysisDir "
                f"sub-directories within the export directory {self.fspath}"
            )
        return True

    @property
    def t2k_files(self) -> dict[str, T2k]:
        """Hand-held single-lesion captures, keyed by capture timestamp."""
        return {p.stem: T2k(p) for p in self.fspath.glob("*.t2k")}

    @property
    def three_d_capture_dirs(self) -> dict[str, ThreeDCaptureDir]:
        """Whole-body 3D stereo-photogrammetry captures, keyed by capture
        timestamp."""
        return {
            p.name: ThreeDCaptureDir(p)
            for p in self.fspath.iterdir()
            if p.is_dir() and ThreeDCaptureDir.matches(p)
        }

    @property
    def lesion_analysis_dirs(self) -> dict[str, LesionAnalysisDir]:
        """Vectra/Dexi lesion analyses, keyed by capture timestamp."""
        return {
            p.name: LesionAnalysisDir(p)
            for p in self.fspath.iterdir()
            if p.is_dir() and LesionAnalysisDir.matches(p)
        }
