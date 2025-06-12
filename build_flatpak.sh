#!/bin/bash
""":"

# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_DIR=$SCRIPT_DIR


if [ -z $FLATPAK_REPO_DIR ];then
  echo 'Please define `FLATPAK_REPO_DIR`'
exit 1
fi



## Prerequisites
flatpak install -y --user flathub org.flatpak.Builder
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub com.riverbankcomputing.PyQt.BaseApp/x86_64/6.8

## Flatpak Manifest
## Collect Python Packages
python_packages=$(while IFS= read -r line; do
  [[ $line == PyQt* ]] && continue # skip PyQt cause we're using a PyQt base
  printf '%s ' "$line"
done < src/qr_scangen/requirements.txt)
flatpak_pip_generator $python_packages
# validate Flatpak Manifest
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest tech.emendir.QR-ScanGen.yml

# generate MetaInfo XML file  
python generate_metainfo.py pyproject.toml tech.emendir.QR-ScanGen  tech.emendir.QR-ScanGen.metainfo.xml
# validate MetaInfo XML file  
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream tech.emendir.QR-ScanGen.metainfo.xml


# flatpak-builder --user --install  --install-deps-from=flathub --force-clean build-dir tech.emendir.QR-ScanGen.yml
flatpak run org.flatpak.Builder --force-clean --sandbox --user --install --install-deps-from=flathub --ccache --mirror-screenshots-url=https://dl.flathub.org/media/ --repo=$FLATPAK_REPO_DIR build-dir tech.emendir.QR-ScanGen.yml

flatpak build-export $FLATPAK_REPO_DIR build-dir
flatpak build-bundle $FLATPAK_REPO_DIR dist/qr_scangen-current.flatpak tech.emendir.QR-ScanGen 








exit 0
"""
import os
import sys

# Python: re-execute the script in Bash
os.execvp("bash", ["bash", __file__] + sys.argv[1:])
