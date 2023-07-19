#!/bin/bash
# `pip freeze > 0_freeze.txt` to generate dependencies
# run `. ./0_bash.sh` in your terminal to get started

# set paths
if test -d "0_scripts" ; then wd="0_scripts" ; else wd="." ; fi
pev="python_environment"
act="bin/activate"
# create venv if it does not exist
if test ! -e "$wd/$pev/$act" ; then
	echo "Creating venv..."
	python -m venv "$wd/$pev"
	req="yes" ; fi
# activate venv
echo "Setting up venv..."
source "$wd/$pev/$act"
echo -n ' `pip` is now: '
which pip
# install requirements if venv newly created
if test -n "$req" ; then
	pip install --user -r "$wd/0_freeze.txt" ; fi
