#!/bin/sh
if [ "$#" -gt 1 ]; then
    python3 rushour3.py "$1" "$2"
else
    python3 rushhour3.py "$1"
fi