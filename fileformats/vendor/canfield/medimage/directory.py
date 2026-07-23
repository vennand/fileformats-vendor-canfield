from fileformats.core import mtime_cached_property, validated_property
from fileformats.core.exceptions import FormatMismatchError
from fileformats.generic import Directory, UnicodeFile
from fileformats.application import Json, Xml
from fileformats.image import Jpeg, Svg, Png


class DexiDir(Directory):
    """Canfield Dexi image data directory

    Canfield encrypted proprietary image file format.
    """

    @mtime_cached_property
    def result_dict(self) -> dict:
        """The results file in the directory."""
        return self.result_file.load()

    @validated_property  # validated_property is checked at initialization time, so if this file is missing the format will not match
    def result_file(self) -> Json:
        """The results file in the directory."""
        return Json(self.fspath / "result.json")

    # Alternatively to the implementation below, we could just find and return
    # the files from their extensions in the directory. If there is a case
    # where there might be different output files we could just collapse
    # these properties into
    # a single validated property called 'output_files' or something

    @validated_property
    def heatmap_file(self) -> Jpeg:
        """The heatmap file in the directory."""
        return Jpeg(
            self.fspath / self.result_dict["OutputFiles"]["HeatMap"]
        )  # FIXME: I don't have the exact path for this

    @validated_property
    def lesion_file(self) -> Svg:
        """The lesion file in the directory."""
        return Svg(
            self.fspath / self.result_dict["OutputFiles"]["Lesion"]
        )  # FIXME: I don't have the exact path for this


class DanaosDir(Directory):
    """Canfield Danaos image data directory

    Canfield encrypted proprietary image file format.
    """

    @validated_property
    def asymmetry_files(self) -> list[Png]:
        """The asymmetry files in the directory."""
        return [Png(self.fspath / f) for f in self.fspath.glob("Asy*.png")]

    @validated_property
    def colour_files(self) -> list[Png]:
        """The colour files in the directory."""
        return [Png(self.fspath / f) for f in self.fspath.glob("Col*.png")]

    @validated_property
    def contour_file(self) -> list[Png]:
        """The colour files in the directory."""
        return Png(self.fspath / "Cont.png")

    @validated_property
    def data_file(self) -> Xml:
        """The data file in the directory."""
        return Xml(self.fspath / "Data.xml")

    @validated_property
    def hair_file(self) -> Png:
        """The hair file in the directory."""
        return Png(self.fspath / "Hair.png")


class Vectra(Directory):
    """Canfield Vectra image data directory

    Canfield encrypted proprietary image file format.
    """

    @validated_property
    def catpureinfo_file(self) -> UnicodeFile:
        """The capture info file in the directory."""
        return UnicodeFile(self.fspath / "catpureinfo_scope")

    @validated_property
    def danaos_dir(self) -> DanaosDir:
        """The danaos directory in the directory."""
        return DanaosDir(self.fspath / "DANAOS")

    @validated_property
    def dexi_dirs(self) -> dict[str, DexiDir]:
        """Dictionary of dexi directories sorted by their version."""
        dct = {
            p.name.split("_")[1]: DexiDir(p)
            for p in self.fspath.glob("DexiData_*")
            if p.is_dir()
        }
        if not dct:
            raise FormatMismatchError(
                f"Did not find any DexiData sub-directories within the Vectra directory path {self.fspath}"
            )
        return dct
