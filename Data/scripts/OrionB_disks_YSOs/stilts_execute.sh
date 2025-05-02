#!/bin/zsh

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
