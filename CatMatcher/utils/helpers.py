import os


def set_run_path(subdir: str, script_path: str= "../Data/scripts/"):
    """
    Automatically sets the output directory to a folder named after the current date.
    :param script_name: enable further creation of a subdirectory with the name of the script (for clarity)
    :param main_path: Path to the directory containing the coding-logs
    :return: path-string
    """
    output_path = script_path + subdir
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass
    output_path = output_path + "/"

    return output_path
