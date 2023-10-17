from __project__ import version, project_name
import shutil
import os
import platform
hidden_imports = [
    "pywifi",
    "pyzbar",
    "qrcode",
]
# converting *.ui files to *.py files
for dirname, dirnames, filenames in os.walk("."):
    if dirname == "./Plugins" or "./.git" in dirname:
        continue
    for filename in filenames:
        path = os.path.join(dirname, filename)
        if(filename[-2:] == "ui"):
            print(filename)
            os.system(f"pyuic5 {path} -o {path[:-2]}py")
if os.path.exists("build"):
    shutil.rmtree("build")
# shutil.rmtree("dist")

if (platform.system().lower() == "windows"):
    cmd = f"pyinstaller --name={project_name} --windowed --onefile --add-data=Icon.svg;. __main__.py"
    for lib in hidden_imports:
        cmd += f" --hidden-import={lib}"
    import pyzbar
    pyzbardir = os.path.dirname(pyzbar.__file__)
    cmd += f" --add-binary={pyzbardir}\\libiconv.dll;."
    cmd += f" --add-binary={pyzbardir}\\libzbar-64.dll;."
    os.system(cmd)
    shutil.move(os.path.join("dist", f"{project_name}.exe"),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.exe"))
else:
    cmd = f"pyinstaller --name='{project_name}' --windowed --onefile --add-data='Icon.svg:.' __main__.py"
    for lib in hidden_imports:
        cmd += f" --hidden-import={lib}"
    cmd = "export QT_DEBUG_PLUGINS=1;"+cmd
    print(cmd)
    os.system(cmd)
    shutil.move(os.path.join("dist", project_name),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.AppImage"))
