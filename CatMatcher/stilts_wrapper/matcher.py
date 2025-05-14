import os
import stat
import pandas as pd

from CatMatcher.stilts_wrapper.match_configurator import MatchConfigurator
from CatMatcher.stilts_wrapper.shell_helper import execute_shell_script


class StiltsMatcher(MatchConfigurator):

    def set_relative_paths(self):
        """
        Path setter for relative path variables for STILTS.

        It is important to note, that the paths in the command-file need to be relative to the location of the script files.
        Currently, this structure is hardcoded in the following way:
        ├── Data directory (where all the files are)
        │   └── CatMatcher_cwd
        │        ├── scripts
        │            ├── match_commands.txt
        │            └── stilts_execute.sh
        │        ├── matches
        │            └── match file(s)
        :return: Relative paths for input and output files
        """

        relative_data_output_path = self._matched_path + self.output_file_name

        if not self.data_dir:

            f = self.file_list[1]

            if self.normalized_path.endswith("/"):
                data_dir = self.normalized_path.split("/")[-2]

            else:
                data_dir = self.normalized_path.split("/")[-2]

            print(
                f"Data directory name inferered as: {data_dir}. If this is not right, please set the variable manually when"
                f"calling StiltsMatcher.")

        else:
            data_dir = self.data_dir

        # TODO: Quick fix
        relative_data_input_path = f"../../"
        relative_data_output_path = "../matches/"

        return relative_data_input_path, relative_data_output_path

    '''
    def build_simple_pairmatch(self, return_command:bool = False):
        """


        :return:
        """


        if self.reference_file is not None:
            files = [self.reference_file, self.file_list]
        else:
            files = self.file_list
        # First line of the command (static)
        command = (
            f"stilts tmatchn multimode={self.multimode} nin={self.n_in} matcher={self.matcher} params={self.match_radius} \\\n"
        )

        # Iteratively add in{x}, ifmt{x}, suffix{x}, values{x} for each file
        for idx, file in enumerate(files, start=1):
            command += (
                f"\tin{idx}={os.path.join(rel_data_in, file)} ifmt{idx}={self.ifmt} "
                f"suffix{idx}='_{self.suffix_list[idx - 1]}' values{idx}='{self.match_values}' \\\n"
            )
            print(idx, file)

        # iteratively add the join statements
        for idx, file in enumerate(files, start=1):
            if idx == 1:
                command += (
                    f"\tjoin{idx}={self.join_mode} ")
            else:
                command += (
                    f"join{idx}={self.join_mode} ")

        # Final line of the command
        if self.output_command is not None:
            command += (
                f"\\\n"
                f"\tfixcols={self.fixcols} ocmd={self.output_command} out={os.path.join(rel_data_out, self.output_file)} ofmt={self.ofmt} progress={self.progress}"
            )
        else:
            command += (
                f"\\\n"
                f"\tfixcols={self.fixcols} out={os.path.join(rel_data_out, self.output_file)} ofmt={self.ofmt} progress={self.progress}"
            )

        # Write the command to a shellscript file

            with open(os.path.join(rel_data_out, self.output_file), 'w') as file:
                file.write(command)
                print(f"Command written to {self.output_path}")
            os.chmod(self.output_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        else:
            print(command)
    '''

    def build_N_match(self, print_command: bool = False):

        rel_data_in, rel_data_out = self.set_relative_paths()
        print(rel_data_in)

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
                        f"\tin{idx}={rel_data_in +file} ifmt{idx}={self.ifmt[idx - 1]} "
                        f"suffix{idx}='_{suffix}' "
                        f"values{idx}='{self.match_values[idx - 1]}' \\\n"
                    )

            # Command if 1 match column(=same name in all files) and n formats are given
            elif len(self.match_values) == 1 and len(self.ifmt) == self.n_in:

                for idx, file in enumerate(self.file_list, start=1):
                    suffix = self.suffix_list[idx - 1]
                    command += (
                        f"\tin{idx}={rel_data_in+ file} ifmt{idx}={self.ifmt[idx - 1]} "
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

        # TODO: Careful - quick fix here
        # Add the rest of the fixed part of the command
        command += (
            f"\\\n"
            f"\tfixcols={self.fixcols} out={'../matches/' + self.output_file_name} ofmt={self.ofmt} progress={self.progress}"
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

        # create the command
        self.build_N_match()

        # run the stilts script
        execute_shell_script(destination_path=self._script_path, return_output=return_output)

        # log
        # if log_file:
        # TODO: Function for creating log with match-params and match statistic
