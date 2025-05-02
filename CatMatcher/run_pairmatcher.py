from stilts_wrapper.matcher import StiltsMatcher


# matcher.build_simple_pairmatch()

matcher = StiltsMatcher(
    reference_file="test.csv",
    file_list="match_file.csv",
    output_file="matched.csv",
    suffix_list=["a", "b"],
    rel_dir="../data/",
    match_radius=0.5,
   # n_in=2,
    output_path="../Data/scripts/match_commands.txt",
)

