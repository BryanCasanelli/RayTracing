#!/bin/sh
if command -v python3 &>/dev/null; then
    python3 source/RayTracing.py
else
    echo "Python 3 is not installed. Please install Python 3 to run this script."
fi
