import os
import stat

from CatMatcher.match_configurator import MatchConfigurator
from CatMatcher.shell_helper import execute_shell_script


class StiltsMatcher(MatchConfigurator):
    """
    This class is used build and execute the STILTS `tmatchN` function based on the provided matching configuration ( see `MatchConfigurator`).

    It inherits from `MatchConfigurator` and automates the generation of STILTS commands used to perform
    multi-table astronomical catalog matching.

    .. note::

        It is important to note that the paths in the command file must be relative to the location of the script files.
        The folder structure is hardcoded as follows::

            ├── Data directory (where all the files are)
            │   └── CatMatcher_cwd
            │        ├── scripts
            │            ├── match_commands.txt
            │            └── stilts_execute.sh
            │        ├── matches
            │            └── match file(s)
   """

    def build_N_match(self, print_command: bool = False):
        """
        Builds the full STILTS tmatchn command for N-way matching of input catalogs and writes it to a shell-executable file.

        This method uses the match attributes described in the `MatchConfigurator` dataclass, like input files, formats, suffixes, match values, to construct a command file for the STILTS software, which can be run via the terminal. It handles all combinations of match column and format configurations that the author could think of until now :P (e.g., one for all files or distinct per file).

        The command is written to `command_file_name` inside the `scripts/` directory and made executable. Note that,
        depending on the individual user system settings, the action of making the file executable might require root privileges.

        Args:
            print_command (bool): If True, prints the final command to stdout for user inspection.

        Returns:
            No direct output, but:

            - Writes the constructed command string to a `.txt` file (and prints it if required).
            - Makes the command file executable via `chmod`.
        """

        # define relative paths
        rel_data_in = f"../../"
        rel_data_out = "../matches/"

        # Start the command
        command = (
            f"stilts tmatchn multimode={self.multimode} nin={self.n_in} matcher={self.matcher} params={self.match_radius} \\\n"
        )

        # Command including the suffix information
        if self.suffix_list is not None:

            # Command if n match columns and n formats are given
            if len(self.match_values) == self.n_in and len(self.ifmt) == self.n_in:

                # Iteratively add in{x}, ifmt{x}, suffix{x}, values{x} for each file
                for idx, file in enumerate(self.file_list, start=1):
                    suffix = self.suffix_list[idx - 1]
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[idx - 1]} "
                        f"suffix{idx}='_{suffix}' "
                        f"values{idx}='{self.match_values[idx - 1]}' \\\n"
                    )

            # Command if 1 match column(=same name in all files) and n formats are given
            elif len(self.match_values) == 1 and len(self.ifmt) == self.n_in:

                for idx, file in enumerate(self.file_list, start=1):
                    suffix = self.suffix_list[idx - 1]
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[idx - 1]} "
                        f"suffix{idx}='_{suffix}' "
                        f"values{idx}='{self.match_values[0]}' \\\n"
                    )

            # Command if n match columns and 1 format (same for all files) are given
            elif len(self.match_values) == self.n_in and len(self.ifmt) == 1:

                for idx, file in enumerate(self.file_list, start=1):
                    suffix = self.suffix_list[idx - 1]
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[0]} "
                        f"suffix{idx}='_{suffix}' "
                        f"values{idx}='{self.match_values[idx - 1]}' \\\n"
                    )

            elif len(self.match_values) == 1 and len(self.ifmt) == 1:

                for idx, file in enumerate(self.file_list, start=1):
                    suffix = self.suffix_list[idx - 1]
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[0]} "
                        f"suffix{idx}='_{suffix}' "
                        f"values{idx}='{self.match_values[0]}' \\\n"
                    )

        # Same as above but without specifying the suffix line
        elif self.suffix_list is None:

            if len(self.match_values) == self.n_in and len(self.ifmt) == self.n_in:

                for idx, file in enumerate(self.file_list, start=1):
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[idx - 1]} "
                        f"values{idx}='{self.match_values[idx - 1]}' \\\n"
                    )

            elif len(self.match_values) == 1 and len(self.ifmt) == self.n_in:

                for idx, file in enumerate(self.file_list, start=1):
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[idx - 1]} "
                        f"values{idx}='{self.match_values[0]}' \\\n"
                    )

            elif len(self.match_values) == self.n_in and len(self.ifmt) == 1:

                for idx, file in enumerate(self.file_list, start=1):
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[0]} "
                        f"values{idx}='{self.match_values[idx - 1]}' \\\n"
                    )

            elif len(self.match_values) == 1 and len(self.ifmt) == 1:

                for idx, file in enumerate(self.file_list, start=1):
                    command += (
                        f"\tin{idx}={rel_data_in + file} ifmt{idx}={self.ifmt[0]} "
                        f"values{idx}='{self.match_values[0]}' \\\n"
                    )

        # iteratively add the join statements
        for idx, file in enumerate(self.file_list, start=1):
            if (idx == 1) or (idx == int(len(self.file_list) / 2) + 1):
                command += (
                    f"\tjoin{idx}={self.join_mode} ")
            elif idx == int(len(self.file_list) / 2):
                command += (
                    f"join{idx}={self.join_mode} \\\n")
            else:
                command += (
                    f"join{idx}={self.join_mode} ")

        # Add the rest of the fixed part of the command
        command += (
            f"\\\n"
            f"\tfixcols={self.fixcols} out={rel_data_out + self.output_file_name} ofmt={self.ofmt} progress={self.progress}"
        )

        # Write the command to the file

        # set default command file name
        if self.command_file_name is None:
            self.command_file_name = "Nmatch_commands.txt"

        with open(os.path.join(self._script_path, self.command_file_name), 'w') as file:
            file.write(command)
            print(f"Command written to {self._script_path + self.command_file_name}")
        os.chmod(self._script_path + self.command_file_name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        if print_command:
            print(command)

    def perform_Nmatch(self, return_output: bool = True, log_file: bool = True):
        """
         Executes the STILTS match command constructed by `build_N_match`.

         This method calls `build_N_match()` to prepare the matching script, then executes it using a shell call.
         Optionally returns output logs and is intended to support future logging of match parameters and statistics.

         Args:
             return_output (bool): If True, prints shell execution output and error to stdout.
             log_file (bool): Placeholder for future implementation of a match log generation function.

         Returns:
            No direct output, but:
             - Writes the constructed command string to a `.txt` file (and prints it if required).
             - Executes a shell script to perform the match.
             - (Planned) Generates a log file with match parameters and statistics.
         """

        # create the command
        self.build_N_match()

        # run the stilts script
        execute_shell_script(destination_path=self._script_path, return_output=return_output)

        # log
        # if log_file:
        # TODO: Function for creating log with match-params and match statistic
