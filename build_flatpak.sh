#!/bin/bash
""":"

flatpak-builder --user --install --force-clean build-dir flatpak.yaml









exit 0
"""
import os
import sys

# Python: re-execute the script in Bash
os.execvp("bash", ["bash", __file__] + sys.argv[1:])
