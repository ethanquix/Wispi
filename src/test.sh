#!/bin/sh

echo "Usage: ./test.sh [codecov repository token]"

echo "Testing..."

if [ "$#" -ne 1 ]; then
    echo "No token mode selected (without coverage)"
    coverage run --source . testAll.py
    coverage report
else
    echo "Token mode selected (with coverage)"
    coverage run testAll.py
    codecov --token=$1
fi