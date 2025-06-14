#!/bin/python
""":"
# Shell: re-execute this script with Python
exec python3 "$0" "$@"
exit 0
"""

import shutil
import os
import platform
import toml
HIDDEN_IMPORTS = [
    "pywifi",
    "pyzbar",
    "qrcode",
]
EXCLUDED_IMPORTS = [
    "PyQt5"
]


WORK_DIR = os.path.dirname(__file__)
PROJ_DIR=os.path.abspath(os.path.join(WORK_DIR, "..", ".."))
SOURCE_DIR = os.path.join(PROJ_DIR, "src")
ENTRY_POINT = os.path.join(SOURCE_DIR, "__main__.py")

DATA_FILES = [
    os.path.join("qr_scangen", "Icon.svg")
]


with open(os.path.join(PROJ_DIR,'pyproject.toml'), 'r') as file:
    data = toml.load(file)
    project_name = data['project']['name']
    version = data['project']['version']
    
# converting *.ui files to *.py files
for dirname, dirnames, filenames in os.walk("."):
    if dirname == "./Plugins" or "./.git" in dirname:
        continue
    for filename in filenames:
        path = os.path.join(dirname, filename)
        if (filename[-2:] == "ui"):
            print(filename)
            os.system(f"pyuic6 {path} -o {path[:-2]}py")
if os.path.exists("build"):
    shutil.rmtree("build")
# shutil.rmtree("dist")
command_appendages = ""
for lib in HIDDEN_IMPORTS:
    command_appendages += f" --hidden-import={lib}"
for lib in EXCLUDED_IMPORTS:
    command_appendages += f" --exclude={lib}"
for file in DATA_FILES:
    command_appendages += (
        f" --add-data='{os.path.join(SOURCE_DIR, file)}:"
        # f"{os.path.dirname(file)}'"
        ".'"
    )


if (platform.system().lower() == "windows"):
    cmd = (
        f"pyinstaller --name={project_name} --windowed --onefile "
        f"{ENTRY_POINT} {command_appendages}"
    )

    import pyzbar
    pyzbardir = os.path.dirname(pyzbar.__file__)
    cmd += f" --add-binary={pyzbardir}\\libiconv.dll;."
    cmd += f" --add-binary={pyzbardir}\\libzbar-64.dll;."
    os.system(cmd)
    shutil.move(os.path.join("dist", f"{project_name}.exe"),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.exe"))
else:
    cmd = (
        f"pyinstaller --name={project_name} --windowed --onefile "
        f"{ENTRY_POINT} {command_appendages}"
    )
    cmd = "export QT_DEBUG_PLUGINS=1;" + cmd
    print(cmd)
    os.system(cmd)
    shutil.move(os.path.join("dist", project_name),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.AppImage"))
