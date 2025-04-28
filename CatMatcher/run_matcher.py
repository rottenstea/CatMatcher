from stilts_wrapper.matcher import StiltsMatcher

matcher = StiltsMatcher(
    reference_file="test.csv",
    match_file="match_file.csv",
    output_file="matched.csv",
    suffix=["a", "b"],
    rel_dir="../data/",
    match_radius=0.5,
    n_in=2,
    output_path="../Data/scripts/match_commands.txt",
)


matcher.build_simple_pairmatch()