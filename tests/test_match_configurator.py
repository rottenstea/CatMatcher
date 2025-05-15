import re
import pytest
import numpy as np
from src.CatMatcher import MatchConfigurator  # Replace with actual import


def generate_dummy_class():
    """ Generate dummy class instance with the required user input values to use for class method testing."""
    return MatchConfigurator(file_list=["a.csv", "b.csv", "c.csv"], output_file="test.csv", output_path="test_path",
                             rel_dir="rel_dir", match_radius=0.1)


def test_infer_fmt_valid_formats():
    """Check that the _infer_fmt function actually grabs the right part of the file and compares
    it to the supported formats."""

    mc = generate_dummy_class()

    valid_formats = ["colfits", "csv", "ecsv", "fits", "tst", "votable"]

    for fmt in valid_formats:
        filename = f"example.{fmt}"
        assert mc._infer_fmt(filename) == fmt


def test_infer_fmt_multiple_extensions():
    """ Check that for edge case files with multiple extensions, which are separated by dots
    (happens e.g., with fits files) always the last extension is considered"""

    mc = generate_dummy_class()

    assert mc._infer_fmt("fits_table.ptable.fits") == "fits"


def test_infer_fmt_unsupported_filetype():
    """ Check that ValueError is raised reliably when trying to use an unsupported file format as input """

    mc = generate_dummy_class()

    test_file = "test.txt"

    expected_message = f"Unsupported file format 'txt'. Allowed formats are: ['colfits', 'csv', 'ecsv', 'fits', 'tst', 'votable']"
    with pytest.raises(ValueError, match=re.escape(expected_message)):
        mc._infer_fmt(test_file)


def test_infer_fmt_no_filetype():
    """ Check that ValueError is raised when no extension is found"""

    mc = generate_dummy_class()

    test_file = "test"

    with pytest.raises(ValueError, match="No extension found"):
        mc._infer_fmt(test_file)


def test_post_init_automatic_variable_inferrence():
    """ Check that the _post_init function automatically infers the file number and suffix list from
    the input, if not user-specified."""

    mc = MatchConfigurator(reference_file="ref.fits", file_list=["a.csv", "b.csv", "c.csv"], output_file="test.csv",
                           output_path="test_path",
                           rel_dir="rel_dir", match_radius=0.1)

    assert mc.n_in == 3
    assert mc.suffix_list == ["1", "2", "3"]
    assert mc.ofmt == "csv"
    assert mc.ifmt == "fits"


def test_post_init_keep_user_suffixes():
    """ Check that if a suffix list is given, the _post_init function does not override it"""

    mc = MatchConfigurator(file_list=["a.csv", "b.csv", "c.csv"], output_file="test.csv", output_path="test_path",
                           rel_dir="rel_dir", match_radius=0.1, suffix_list=["aa", "bb", "cc"])
    assert mc.suffix_list == ["aa", "bb", "cc"]


def test_post_init_suffix_list_size_smaller_than_filelist():
    """ Check that ValueError with message is raised when the number of suffixes provided by the user is
     SMALLER than the number of provided files."""

    with pytest.raises(ValueError, match="Length of suffix-list does not match number of input files."):
        assert MatchConfigurator(file_list=["a.csv", "b.csv", "c.csv"], output_file="test.csv", output_path="test_path",
                                 rel_dir="rel_dir", match_radius=0.1, suffix_list=["aa", "bb"])


def test_post_init_suffix_list_size_bigger_than_filelist():
    """ Check that ValueError with message is raised when the number of suffixes provided by the user is
     BIGGER than the number of provided files."""

    with pytest.raises(ValueError, match="Length of suffix-list does not match number of input files."):
        assert MatchConfigurator(file_list=["a.csv", "b.csv", "c.csv"], output_file="test.csv", output_path="test_path",
                                 rel_dir="rel_dir", match_radius=0.1, suffix_list=["aa", "bb", "cc", "dd"])


def test_NANs_in_input_filelist():
    """ Check that the class correctly handles entries like nans (currently only numpy nans) in the
    input file list by raising an error."""

    with pytest.raises(ValueError, match="Empty strings or NAN entries encountered in input file list."):
        MatchConfigurator(file_list=["a.csv", np.nan, "c.csv"], output_file="test.csv", output_path="test_path",
                          rel_dir="rel_dir", match_radius=0.1, suffix_list=["aa", "bb", "dd"])


def test_empty_strings_in_input_filelist():
    """ Check that the class correctly handles entries like empty strings in the
    input file list by raising an error."""

    with pytest.raises(ValueError, match="Empty strings or NAN entries encountered in input file list."):
        MatchConfigurator(file_list=["a.csv", "", "c.csv"], output_file="test.csv", output_path="test_path",
                          rel_dir="rel_dir", match_radius=0.1, suffix_list=["aa", "bb", "dd"])


def test_NANs_in_suffix_list():
    """ Check that the class correctly handles entries like nans (currently only numpy nans) in the
    suffix list by raising an error."""

    with pytest.raises(ValueError, match="Empty strings or NAN entries encountered in user-provided suffix list."):
        MatchConfigurator(file_list=["a.csv", "b.csv", "c.csv"], output_file="test.csv", output_path="test_path",
                          rel_dir="rel_dir", match_radius=0.1, suffix_list=[np.nan, "bb", "dd"])


def test_empty_strings_in_suffix_list():
    """ Check that the class correctly handles entries like empty strings in the
    suffix list by raising an error."""

    with pytest.raises(ValueError, match="Empty strings or NAN entries encountered in user-provided suffix list."):
        MatchConfigurator(file_list=["a.csv", "b.csv", "c.csv"], output_file="test.csv", output_path="test_path",
                          rel_dir="rel_dir", match_radius=0.1, suffix_list=["aa", "", ""])
