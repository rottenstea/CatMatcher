from stilts_wrapper.matcher import StiltsMatcher

matcher = StiltsMatcher(
    reference_file="test.csv",
    file_list="match_file.csv",
    output_file="matched.csv",
    suffix_list=["a", "b"],
    rel_dir="../data/",
    match_radius=0.5,
   # n_in=2,
   # output_path="../Data/scripts/match_commands.txt",
)


# matcher.build_simple_pairmatch()

Nmatcher = StiltsMatcher(
    file_list=["file1.csv", "file2.csv", "file3.csv"],
    output_file="matched.csv",
    suffix_list=["a", "b", "c"],
    rel_dir="../data/",
    match_radius=0.5,
   # n_in=2,
   # output_path="../Data/scripts/match_commands.txt",
)


Nmatcher._generate_match_values_from_suffix()


Nmatcher.build_N_match()

