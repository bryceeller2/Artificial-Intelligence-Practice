#!/bin/sh
if [ "$#" -gt 1 ];
then
 python3 rushhour2.py "$1" "$2"
else
 python3 rushhour2.py "$1"
fi