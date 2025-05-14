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


def setup_stilts_directory(file_path:str, cwd_name:str = None,  return_paths: bool = False):

    # Set default directory name if no name is provided by the user
    if not cwd_name:
        cwd_name = "CatMatcher_cwd"

    # create filepath
    if file_path.endswith("/"):  # no need to add the slash if provided in the path name
        cwd_path = file_path + cwd_name
    else:
        cwd_path = file_path + "/" + cwd_name  # if pathname does not include slash, add it

    # Create various subdirectories
    script_dir = cwd_path + "/scripts/"
    match_dir = cwd_path + "/matches/"

    # store in directory_list
    dirs = [cwd_path, script_dir, match_dir]

    for d in dirs:
        try:
            os.mkdir(d)
        except FileExistsError:
            pass

    if return_paths:
        return dirs
