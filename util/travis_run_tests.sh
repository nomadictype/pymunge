#!/bin/bash

PEP8=--pep8

if [ "${TRAVIS_PYTHON_VERSION}" = "3.3" ]; then
	echo "Disabling PEP8 check on Python 3.3"
	PEP8=
fi

coverage run --source pymunge -m pytest ${PEP8}
