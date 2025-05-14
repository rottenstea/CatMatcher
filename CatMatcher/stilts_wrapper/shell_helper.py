import os
import stat
import subprocess


def spawn_shell_script(destination_path: str, name: str, content: str):
    """
    Creates and saves a shell script file to the specified destination with executable permissions.

    If no content is provided, a default zsh (korn-shell, standard for macOS systems) script is written that:
    - Sources `~/.zshrc`
    - Prints the current working directory (cwd) (currently used only as fail-save for verification purposes)
    - Loops over `.txt` files at the cwd and executes them if executable

    Args:
        destination_path (str): Path where the script will be saved.
        name (str): Name of the script file to create.
        content (str): The content of the shell script. If None, the default script is used.

    Returns:
        None
    """

    script_name = name
    file_path = destination_path + script_name

    if content is None:
        script_content = '''#!/bin/zsh

# Source the ~/.zshrc file
source ~/.zshrc

# Print the current working directory
echo "Current directory: $(pwd)"

# Loop through all .txt files and execute them if they are executable
for file in *.txt; do
    if [ -x "$file" ]; then
        ./"$file"
    else
        echo "$file is not executable"
    fi
done
'''
    else:
        script_content = content

    # Save the shell script to the directory
    with open(file_path, 'w') as script_file:
        script_file.write(script_content)

    # Make the script executable
    os.chmod(file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)


def execute_shell_script(destination_path: str, name: str = "stilts_execute.sh", content: str = None, shell="zsh",
                         return_output: bool = False):
    """
    Creates and executes a shell script in a specified directory.

    This function first generates a shell script by calling the `spawn_shell_script` function, then runs it using
    the specified shell (default is `zsh`). Optionally, the output and errors of the script execution
    can be printed.

    Args:
        destination_path (str): Directory where the script will be created and executed.
        name (str, optional): Name of the shell script file. (Default: "stilts_execute.sh")
        content (str, optional): Custom content for the shell script. If None, a default is used. See `spawn_shell_script`
        for details on the default script content.
        shell (str, optional): Shell to use for execution (e.g., "zsh", "bash"). Defaults to "zsh".
        return_output (bool, optional): Whether to print stdout, stderr, and return code. Defaults to False.

    Returns:
        None
    """
    spawn_shell_script(destination_path, name, content)
    result = subprocess.run([shell, name], cwd=destination_path, capture_output=True, text=True)

    if return_output:
        print('Output:', result.stdout)
        print('Error:', result.stderr)
        print('Return code:', result.returncode)


