#!/bin/bash

word="start"

for file in *; do
    if [ -f "$file" ]; then
        grep "$word" "$file" | tail -n 1 | awk -v file="$file" '{print file ": " $0}'
    fi
done
