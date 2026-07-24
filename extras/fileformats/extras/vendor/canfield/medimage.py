import os
import typing as ty
from fileformats.core import extra_implementation
from fileformats.medimage.base import MedicalImagingData


@extra_implementation(MedicalImagingData.deidentify)
def deidentify_export_dir(
    self: MedicalImagingData,
    spec: ty.Any = None,
    out_dir: os.PathLike[str] | None = None,
) -> tuple[MedicalImagingData, ty.Mapping[str, ty.Any]]:
    """
    Deidentifies the image by stripping any subject-identifying information from the
    image header. The exact implementation of this method will depend on the
    specific image format and the type of identifying information that is present. The
    output files should be named with a new file path(s) that is derived from the metadata,
    such that it doesn't contain any subject-identifying information within it.

    Parameters
    ----------
    spec: Any, optional
        A specification for the deidentification process, which may include details on
        which fields to remove or how to handle certain types of data. The exact
        structure of this specification will depend on the specific image format and the
        type of identifying information that is present.
    out_dir: PathLike, optional
        The directory where the deidentified files should be written. If not provided,
        a default location will be used.

    Returns
    -------
    tuple[MedicalImagingData, Mapping[str, Any]]
        A tuple containing the deidentified MedicalImagingData object and a mapping of
        any relevant metadata or information about the deidentification process.
    """
    # Implement the deidentification logic here, based on the specific format and requirements.
    # This is a placeholder implementation and should be replaced with actual logic.
    raise NotImplementedError(
        "Deidentification logic for ExportDir is not implemented yet."
    )
