import os
from CatMatcher.matcher import StiltsMatcher

""" This script runs the minimum viable product of the CatMatcher routine, as of 14-05-2025. It takes in a
number of files  and matches them based on the column names and matching radius provided by the user."""

# 1. Indicate file location
file_path = 'Data/example_files/'
files = sorted([f for f in os.listdir(file_path) if "csv" in f])  # grab desired files at the file_path

# Optional:
suffixes = [name.split("_")[0] for name in files]  # Can also be an arbitrary list, if omitted will be _1, _2, ...

# 2. Define Match parameters
match_kwargs = dict(
    match_values=["RAJ2000 DEJ2000", "RAJ2000 DEJ2000", "RA DE"],  # Names of the columns to match
    match_radius=1,  # arcseconds,
    join_mode="match",  # only keep rows that appear in all catalogs
)

# 3. Initialize Matcher
Nmatcher = StiltsMatcher(
    file_list=files,
    file_path=file_path,
    output_file_name="tst2.csv",  # Optional: name of the output file
    command_file_name="N_match_commands_t2.txt",  # Optional
    suffix_list=suffixes,  # Optional
    **match_kwargs)

# 4. Perform match
Nmatcher.perform_Nmatch()
