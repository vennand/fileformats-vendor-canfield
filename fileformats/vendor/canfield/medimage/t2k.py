from fileformats.generic import BinaryFile


class T2k(BinaryFile):
    """Canfield Vectra image data for the ACEMID (Australian Centre of
    Excellence in Melanoma Imaging and Diagnosis) project.

    Canfield encrypted proprietary image file format.
    """

    ext = ".t2k"
