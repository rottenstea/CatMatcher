import os
from utils.helpers import set_run_path
from stilts_wrapper.matcher import StiltsMatcher

""" This script runs the minimum viable product of the CatMatcher routine, as of 02-05-2025. It takes in a
number of files  and matches them based on the column names and matching radius provided by the user. The result is
saved in the Data/matches/ directory."""

# 1. Define a working directory -- each new match/project should be done in its own subdirectory, as currently the shell
# script grabs all the command files ending in *txt it can find in the working directory and runs them sequentially.
wd_name = "OrionB_disks_YSOs"
shell_script_path = set_run_path(subdir =  wd_name)  # Sets the path and make the directory if it does not exist already

# 2. Indicate file location
file_path = '../Data/example_files/'
files = sorted([f for f in os.listdir(file_path) if "csv" in f])  # grab desired files at the file_path
suffixes=[name.split("_")[0] for name in files]  # Can also be an arbitrary list, if omitted will be _1, _2, ...

# 3. Match parameters
match_values = ["RAJ2000 DEJ2000", "RAJ2000 DEJ2000", "RA DE"]  # Names of the columns to match
match_radius = 1  # arcseconds

# 4. Initialize Matcher
Nmatcher = StiltsMatcher(
    file_list=files,
    output_file_path="../../matches/",  # relative path to the shell script path, where we want the output file
    output_file_name="matched.csv",  # name of the output file
    suffix_list=suffixes,
    rel_dir="../../example_files/",  # relative path to the shell script path, where the files to match are
    ifmt="csv",
    match_radius=match_radius,
    match_values=match_values,
    command_output_path=shell_script_path+"N_match_commands.txt",
)


#Nmatcher.build_N_match()
Nmatcher.perform_Nmatch(script_path=shell_script_path)  # perform match
