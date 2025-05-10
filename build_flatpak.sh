#!/bin/bash
""":"


flatpak install flathub com.riverbankcomputing.PyQt.BaseApp/x86_64/6.8
flatpak-builder --user --install --force-clean build-dir flatpak.yaml









exit 0
"""
import os
import sys

# Python: re-execute the script in Bash
os.execvp("bash", ["bash", __file__] + sys.argv[1:])
