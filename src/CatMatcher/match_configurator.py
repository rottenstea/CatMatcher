import os
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Literal, Union


@dataclass
class MatchConfigurator:
    """
        A configuration class for managing file matching operations using STILTS (Starlink Tables Infrastructure Library Tool Set).

        This class prepares and validates input parameters, infers file formats, and sets up a working directory
        structure for matching catalog files based on various configuration options.

        The first 3 listed attributes need to be defined by the user, whereas all others are either optional or set to
        default values.

        Attributes:
            file_list (Union[list, str]): List of input file names. Alternatively, a single file as a string, but note that this can only be used when a separate reference file is provided. :no-index:
            file_path (str): Path at which the input files are located.
            match_radius (float): Matching radius for positional matching, in arcseconds.
            match_values (Union[str, list], optional): Columns used for matching, default "RA DEC". If the match columns are not identical across all input columns, a list with all the column names, in the same order as the file_list, needs to be provided.

            output_mode (str, fixed): Output mode for the matcher tool. Currently frozen to one specific mode.
            output_file_name (str, optional): Name of the output file to write matched results, including the desired file type. See imft or ofmt for supported filetypes. (Default: "matched.csv)
            command_file_name (str, optional): Name of the command file used to run matching, without suffix. (Default: Nmatch_commands)
            cwd (str, optional): Name of the directory where matching outputs and scripts will be saved.

            matcher (Literal, ["sky", "skyerr", "exact"]): Type of matching engine to use. (Default: "sky")
            multimode (Literal, ["pairs", "group"]): Matching mode, either "pairs" or "group". (Default: "group")
            join_mode (Literal, ["default", "match", "nomatch", "always"]): How results are joined across matched/unmatched catalogs. (Default: "match")
            runner (Literal, ["parallel", "parallel-all", "sequential", "classic", "partest"]): Execution mode for the STILTS matcher. (Default: "parallel")
            progress (Literal, ["none", "log", "time", "profile"]): Logging/progress output during matching. (Default: "time")
            fixcols (Literal, ["none", "dups", "all"]): Determines how input columns are renamed in the output table, according to the suffix_list parameters. If "none", no columns are renamed, if "dups" only columns which would otherwise have duplicate names in the output are renamed, if "all" every column will be renamed.

            reference_file (Optional[str], optional): Optional reference file for input format inference. If provided, a single string input for file_list is acceptable.
            suffix_list (Optional[list], optional): Optional list of suffixes for identifying files. If None, suffixes will be numeric indices _1, _2,... according to the order of the file_list.
            iref (Optional[int], optional): If multimode="pairs" this parameter gives the index of the table in the file_list, which serves as the reference table, i.e. must be matched by other tables.
            input_command (Optional[str], optional): Custom command string indicating actions to be performed on columns of all input tables.
            output_command (Optional[str], optional): Custom command string indicating actions to be performed on columns of the output table.
            ifmt (Optional[list or Literal], ["colfits", "csv", "ecsv", "fits", "tst", "votable"]): Input format(s) for catalog files. Accepted formats are: ["colfits", "csv", "ecsv", "fits", "tst", "votable"]. If not provided, they will be inferred from the file_list.
            ofmt (Optional[Literal], ["colfits", "csv", "ecsv", "fits", "tst", "votable"]): Output format for result file. Accepted formats are: ["colfits", "csv", "ecsv", "fits", "tst", "votable"]. If not provided, it will be inferred from the output_file_name.
        """

    # ---------------------------
    # Minimum necessary user-input
    file_list: Union[list, str]
    file_path: str
    match_radius: float  # params = < match - params >  #TODO: This can also be a list, but in a weird format

    # ----------------------------
    # Variables with default values
    # A) free choice
    match_values: Union[str, list] = "RA DEC"
    output_mode: str = "out"  # There are more options but not needed for now
    output_file_name: str = "matched.csv"
    command_file_name: str = "Nmatch_commands"
    cwd: str = "CatMatcher_cwd"

    # B) Multiple-choice
    matcher: Literal[
        "sky", "skyerr", "exact"] = "sky"  # More available: https://www.star.bris.ac.uk/mbt/stilts/sun256/MatchEngine.html
    multimode: Literal["pairs", "group"] = "group"  # multimode = pairs | group
    join_mode: Literal["default", "match", "nomatch", "always"] = "match"
    runner: Literal["parallel", "parallel-all", "sequential", "classic", "partest"] = "parallel"
    progress: Literal["none", "log", "time", "profile"] = "time"
    fixcols: Literal["none", "dups", "all"] = "dups"
    # TODO: tuning: < tuning - params >

    # ----------------------------
    # Optional
    reference_file: Optional[str] = None
    suffix_list: Optional[list] = None
    iref: Optional[str] = None
    input_command: Optional[str] = None
    output_command: Optional[str] = None
    ifmt: Optional[Literal["colfits", "csv", "ecsv", "fits", "tst", "votable"]] = None
    ofmt: Optional[Literal["colfits", "csv", "ecsv", "fits", "tst", "votable"]] = None

    def __post_init__(self):
        """
        Post-initialization hook to infer further attributes from user input, set up internal variables and the necessary
        directory structure, and validate inputs.
        """

        # ----------------------------
        # A) Infer additional attributes from input variables

        self.command_file = f"{self.command_file_name}.txt"  # ending MUST be .txt
        self.n_in = len(self.file_list)

        # infer suffix list if not provided
        if not self.suffix_list:
            self.suffix_list = [f"{i}" for i in range(1, self.n_in + 1)]
        elif len(self.suffix_list) != self.n_in:
            raise ValueError("Length of suffix-list does not match number of input files.")

        # Infer input format
        if not self.ifmt and self.reference_file:
            self.ifmt = self._infer_fmt(self.reference_file)
        elif not self.ifmt and not self.reference_file:
            self.ifmt = [self._infer_fmt(i) for i in self.file_list]

        # Infer output format
        if not self.ofmt and self.output_file_name:
            self.ofmt = self._infer_fmt(self.output_file_name)

        # ----------------------------
        # B) Convert inputs
        if type(self.ifmt) == str:  # needed for command printing of StiltsMatcher.build_N_match()
            self.ifmt = [self.ifmt]

        if type(self.match_values) == str:  # needed for command printing of StiltsMatcher.build_N_match()
            self.match_values = [self.match_values]

        self.normalized_path = Path(self.file_path).as_posix()  # normalize path (to work across systems)

        # ----------------------------
        # C) Setup directory hierarchy for matching
        self._setup_stilts_directories()

        # ----------------------------
        # D) User input verifications

        # check if file list is valid
        if any(s == "" or (isinstance(s, float) and np.isnan(s)) for s in self.file_list):
            raise ValueError("Empty strings or NAN entries encountered in input file list.")

        # check if suffix list is valid
        if self.suffix_list and any(s == "" or (isinstance(s, float) and np.isnan(s)) for s in self.suffix_list):
            raise ValueError("Empty strings or NAN entries encountered in user-provided suffix list.")

    @staticmethod
    def _infer_fmt(filename):
        """
        Infer the file format from the file extension.

        Args:
            filename (str): The name of the file from which to infer the format.

        Returns:
            str: Inferred file format.

        Raises:
            ValueError: If file has no extension or format is unsupported.
        """

        supported_formats = ["colfits", "csv", "ecsv", "fits", "tst", "votable"]

        fmt = filename.split(".", maxsplit=2)[-1]
        print(fmt, filename.split(".", maxsplit=2))

        if fmt == filename:
            raise ValueError("No extension found")

        if fmt not in supported_formats:
            raise ValueError(f"Unsupported file format '{fmt}'. Allowed formats are: {sorted(supported_formats)}")

        return fmt

    def _generate_match_values_from_suffix(self):
        """
        Generate a list of match columns based on the input string and the supplied suffix list.

        Useful when dealing with more than two input files and a shared base column name.

        Returns:
            None: No direct return, but results are written to self.match_value_list.
        """

        if self.n_in > 2 and type(self.match_values) == str:
            match_columns = self.match_values.split(" ")  # Handles any whitespace-separated values, no number limit
            self.match_value_list = [
                " ".join(f"{val}_{suffix}" for val in match_columns)
                for suffix in self.suffix_list
            ]

    def _setup_stilts_directories(self):
        """
        Create and initialize the working directory structure used by the StiltsMatcher class.

        Directories include the main working path, a scripts directory, and a matches directory.
        """

        # define path to working directory (cwd)
        if self.normalized_path.endswith("/"):  # no need to add the slash if provided in the path name
            cwd_path = self.normalized_path + self.cwd
        else:
            cwd_path = self.normalized_path + "/" + self.cwd  # if pathname does not include slash, add it

        # Create various subdirectories
        script_dir = cwd_path + "/scripts/"
        match_dir = cwd_path + "/matches/"

        # assigin script_path variable because it is needed later to build the N match
        self._script_path = script_dir

        # store in directory_list
        dirs = [cwd_path, script_dir, match_dir]

        # create directories
        for d in dirs:
            try:
                os.mkdir(d)
            except FileExistsError:
                pass
