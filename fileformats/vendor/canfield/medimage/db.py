from fileformats.core.mixin import WithMagicNumber
from fileformats.generic import BinaryFile

import sqlite3


class Vectra_Db(WithMagicNumber, BinaryFile):
    """Canfield Vectra database export for the ACEMID (Australian Centre of Excellence in Melanoma Imaging and Diagnosis) project.

    Vectra partially encrypted database data for reimporting image data into the software.
    """

    ext = ".db"
    # First 16 bytes: "SQLite format 3\0"
    magic_number = b"SQLite format 3\0"