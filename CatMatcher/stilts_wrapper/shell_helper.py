import os
import stat
import subprocess


def spawn_shell_script(destination_path: str, name: str, content: str):
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
    spawn_shell_script(destination_path, name, content)
    result = subprocess.run([shell, name], cwd=destination_path, capture_output=True, text=True)

    if return_output:
        print('Output:', result.stdout)
        print('Error:', result.stderr)
        print('Return code:', result.returncode)


'''
if __name__ == "__main__":
    path = "../data/Catalogs/processed/pype_v2/singles/"
    execute_shell_script(destination_path=path, return_output=True)
'''
