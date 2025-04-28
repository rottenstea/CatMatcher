from stilts_wrapper.match_configurator import MatchConfigurator

config = MatchConfigurator(
    reference_file="test.csv",
    match_file="match_file.csv",
    output_file="match_file.csv",
    rel_dir="../data/",
    match_radius=0.5,
    n_in=2
)