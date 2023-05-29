#!/bin/bash
# run `. ./0_bash.sh`
act="python_environment/bin/activate"
req=""
if test ! -e $act ; then
	echo "Creating venv..."
	python -m venv python_environment
	req="nz" ; fi
echo -n "Setting up venv..."
source $act
echo ' `pip` is now:'
which pip
if test $req ; then
	pip install -r "0_freeze.txt"
else
	echo "If needed, install requirements with 'pip install -r 0_freeze.txt'" ; fi
# pip freeze > 0_freeze.txt
