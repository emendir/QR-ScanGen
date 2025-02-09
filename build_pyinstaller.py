#!/bin/python
""":"
# Shell: re-execute this script with Python
exec python3 "$0" "$@"
exit 0
"""

from metadata import version, project_name
import shutil
import os
import platform
hidden_imports = [
    "pywifi",
    "pyzbar",
    "qrcode",
]
excluded_imports = [
    "PyQt5"
]


WORKDIR=os.path.dirname(__file__)
SOURCE_DIR=os.path.join(WORKDIR, "src")
ENTRY_POINT=os.path.join(SOURCE_DIR,"__main__.py")

DATA_FILES = [
    os.path.join("qr_scangen", "Icon.svg")
]
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
for lib in hidden_imports:
    command_appendages += f" --hidden-import={lib}"
for file in DATA_FILES:
    command_appendages += f" --add-data='{os.path.join(SOURCE_DIR, file)}:{os.path.basename(file)}'"
if (platform.system().lower() == "windows"):
    cmd = f"pyinstaller --name={project_name} --windowed --onefile {ENTRY_POINT} {command_appendages}"
    
    import pyzbar
    pyzbardir = os.path.dirname(pyzbar.__file__)
    cmd += f" --add-binary={pyzbardir}\\libiconv.dll;."
    cmd += f" --add-binary={pyzbardir}\\libzbar-64.dll;."
    os.system(cmd)
    shutil.move(os.path.join("dist", f"{project_name}.exe"),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.exe"))
else:
    cmd = f"pyinstaller --name='{project_name}' --windowed --onefile {ENTRY_POINT} {command_appendages}"
    for lib in hidden_imports:
        cmd += f" --hidden-import={lib}"
    for lib in excluded_imports:
        cmd += f" --exclude={lib}"
    cmd = "export QT_DEBUG_PLUGINS=1;"+cmd
    print(cmd)
    os.system(cmd)
    shutil.move(os.path.join("dist", project_name),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.AppImage"))
