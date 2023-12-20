#!/bin/bash

directory="ptw" # Replace with your directory path
echo "Below is the context: ">all.py

find "$directory" -type f -name "*.py" | while read file; do
    echo "# --- BEGIN - $file ---" >>all.py
    cat "$file">>all.py
    echo "# --- END - $file ---">>all.py
done