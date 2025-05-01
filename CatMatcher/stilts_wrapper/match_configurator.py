import numpy as np
from dataclasses import dataclass
from typing import Optional, Literal, Union


@dataclass
class MatchConfigurator:
    file_list: Union[list,str]
    output_file: str  # out = < out - table >
    output_path: str
    rel_dir: str
    match_radius: float  # params = < match - params >  #TODO: This can also be a list, but in a weird format
    match_values: Union[str, list] = "RA DEC"

    # ----------------------------
    # Multiple-choice
    matcher: Literal[
        "sky", "skyerr", "exact"] = "sky"  # More available: https://www.star.bris.ac.uk/mbt/stilts/sun256/MatchEngine.html
    multimode: Literal["pairs", "group"] = "group"  # multimode = pairs | group
    join_mode: Literal["default", "match", "nomatch", "always"] = "match"
    runner: Literal["parallel", "parallel-all", "sequential", "classic", "partest"] = "parallel"
    progress: Literal["none", "log", "time", "profile"] = "time"
    fixcols: Literal["none", "dups", "all"] = "dups"

    # ----------------------------
    # Fixed (for now)
    output_mode: str = "out"  # There are more options but not needed for now
    # TODO: tuning: < tuning - params >

    # ----------------------------
    # Optional
    reference_file: Optional[str] = None
    suffix_list: Optional[list] = None
    iref: Optional[str] = None
    input_command: Optional[str] = None
    output_command: Optional[str] = None
    ifmt: Optional[Literal["colfits", "csv", "ecsv", "fits", "tst", "votable"]] = None  #TODO: can also be a list of values
    ofmt: Optional[Literal["colfits", "csv", "ecsv", "fits", "tst", "votable"]] = None

    def __post_init__(self):

        # infer n_in
        self.n_in = len(self.file_list)

        # check if file list is valid
        if any(s == "" or (isinstance(s, float) and np.isnan(s)) for s in self.file_list):
            raise ValueError("Empty strings or NAN entries encountered in input file list.")


        # check if suffix list is valid
        if self.suffix_list and any(s == "" or (isinstance(s, float) and np.isnan(s)) for s in self.suffix_list):
            raise ValueError("Empty strings or NAN entries encountered in user-provided suffix list.")



        # infer suffix list if not provided
        if not self.suffix_list:
            self.suffix_list = [f"{i}" for i in range(1, self.n_in + 1)]
        elif len(self.suffix_list) != self.n_in:
            raise ValueError("Length of suffix-list does not match number of input files.")


        # Infer input format
        if not self.ifmt and self.reference_file:
            self.ifmt = self._infer_fmt(self.reference_file)

        # Infer output format
        if not self.ofmt and self.output_file:
            self.ofmt = self._infer_fmt(self.output_file)

    @staticmethod
    def _infer_fmt(filename):
        """Infer file formats from the input and output filenames."""

        supported_formats = ["colfits", "csv", "ecsv", "fits", "tst", "votable"]

        fmt = filename.split(".", maxsplit=2)[-1]

        if fmt == filename:
            raise ValueError("No extension found")

        if fmt not in supported_formats:
            raise ValueError(f"Unsupported file format '{fmt}'. Allowed formats are: {sorted(supported_formats)}")

        return fmt

    def _generate_match_values_from_suffix(self):
        """
        Helper function that can generate a list of match columns based on the input string and the supplied suffix list.
        Probably only for special cases.
        :return: self.match_value_list
        """

        if self.n_in > 2 and type(self.match_values) == str:
            print(self.match_values)

            match_columns = self.match_values.split(" ")  # Handles any whitespace-separated values, no number limit
            self.match_value_list = [
                " ".join(f"{val}_{suffix}" for val in match_columns)
                for suffix in self.suffix_list
            ]



