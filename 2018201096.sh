#!/bin/bash
if [ $# -eq 1 ]; then
	python3 2018201096_2.py $1
else
	python3 2018201096_1.py $1 $2
fi