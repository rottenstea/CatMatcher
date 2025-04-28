from dataclasses import dataclass
from typing import List, Optional, Literal, Union


@dataclass
class MatchConfigurator:
    reference_file: str
    match_file: Union[str, list]
    n_in: float
    suffix = Union[str, list]
    output_file: str  # out = < out - table >
    rel_dir: str
    match_radius: float  # params = < match - params >
    match_values: str = "RA DEC"

    # ----------------------------
    # Multiple-choice
    matcher: Literal[
        "sky", "skyerr", "exact"] = "sky"  # More available: https://www.star.bris.ac.uk/mbt/stilts/sun256/MatchEngine.html
    multimode: Literal["pairs", "group"] = "group"  # multimode = pairs | group
    joinN: Literal["default", "match", "nomatch", "always"] = "match"
    runner: Literal["parallel", "parallel-all", "sequential", "classic", "partest"] = "parallel"
    progress: Literal["none", "log", "time", "profile"] = "time"
    fixcols: Literal["none", "dups", "all"] = "dups"

    # ----------------------------
    # Fixed (for now)
    output_mode: str = "out"  # There are more options but not needed for now

    # ----------------------------
    # Optional
    # TODO: tuning: < tuning - params >
    iref: Optional[str] = None
    input_command: Optional[str] = None
    output_command: Optional[str] = None
    ifmt: Optional[Literal["colfits", "csv", "ecsv", "fits", "tst", "votable"]] = None
    ofmt: Optional[Literal["colfits", "csv", "ecsv", "fits", "tst", "votable"]] = None

    def __post_init__(self):
        # Infer input format
        if not self.ifmt and self.reference_file:
            self.ifmt = self._infer_fmt(self.reference_file)

        # Infer output format
        if not self.ofmt and self.output_file:
            self.ofmt = self._infer_fmt(self.output_file)

    def _infer_fmt(self, filename):
        """Infer file formats from the input and output filenames."""

        supported_formats = ["colfits", "csv", "ecsv", "fits", "tst", "votable"]

        fmt = filename.split(".", maxsplit=2)[-1]
        if fmt not in supported_formats:
            raise ValueError(f"Unsupported file format '{fmt}'. Allowed formats are: {sorted(supported_formats)}")

        return fmt
