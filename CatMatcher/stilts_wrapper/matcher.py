import os
import stat

from CatMatcher.stilts_wrapper.match_configurator import MatchConfigurator


class StiltsMatcher(MatchConfigurator):

    def build_simple_pairmatch(self):

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
                f"\tin{idx}={os.path.join(self.rel_dir, file)} ifmt{idx}={self.ifmt} "
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
                f"\tfixcols={self.fixcols} ocmd={self.output_command} out={self.output_file} ofmt={self.ofmt} progress={self.progress}"
            )
        else:
            command += (
                f"\\\n"
                f"\tfixcols={self.fixcols} out={self.output_file} ofmt={self.ofmt} progress={self.progress}"
            )

        # Write the command to a shellscript file
        if self.output_path is not None:
            with open(self.output_path, 'w') as file:
                file.write(command)
                print(f"Command written to {self.output_path}")
            os.chmod(self.output_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        else:
            print(command)

    def build_N_match(self):

        # Start the command
        command = (
            f"stilts tmatchn multimode={self.multimode} nin={self.n_in} matcher={self.matcher} params={self.match_radius} \\\n"
        )

        if self.match_value_list is not None:

            # Iteratively add in{x}, ifmt{x}, suffix{x}, values{x} for each file
            for idx, file in enumerate(self.file_list, start=1):
                print("file:", file)
                suffix = file.split("_")
                command += (
                    f"\tin{idx}={os.path.join(self.rel_dir, file)} ifmt{idx}={self.ifmt} "
                    f"values{idx}='{self.match_value_list[idx - 1]}' \\\n"
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
            f"\tfixcols={self.fixcols} out={self.output_file} ofmt={self.ofmt} progress={self.progress}"
        )

        # Write the command to the file
        if self.output_path is not None:
            with open(self.output_path, 'w') as file:
                file.write(command)
                print(f"Command written to {self.output_path}")
            os.chmod(self.output_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        else:
            return command
