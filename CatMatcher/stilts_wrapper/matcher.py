import os
import stat

from CatMatcher.stilts_wrapper.match_configurator import MatchConfigurator


class StiltsMatcher(MatchConfigurator):

    def build_simple_pairmatch(self):

        files = [self.reference_file, self.match_file]
        # First line of the command (static)
        command = (
            f"stilts tmatchn multimode={self.multimode} nin={self.n_in} matcher={self.matcher} params={self.match_radius} \\\n"
        )

        # Iteratively add in{x}, ifmt{x}, suffix{x}, values{x} for each file
        for idx, file in enumerate(files, start=1):
            command += (
                f"\tin{idx}={os.path.join(self.rel_dir, file)} ifmt{idx}={self.ifmt} "
                f"suffix{idx}='_{self.suffix[idx-1]}' values{idx}='{self.match_values}' \\\n"
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
