import shutil
import os
import platform
project_name = "QR-ScanGen"
# converting *.ui files to *.py files
for dirname, dirnames, filenames in os.walk("."):
    if dirname == "./Plugins" or "./.git" in dirname:
        continue
    for filename in filenames:
        path = os.path.join(dirname, filename)
        if(filename[-2:] == "ui"):
            print(filename)
            os.system(f"pyuic5 {path} -o {path[:-2]}py")
# shutil.rmtree("dist")

if (platform.system().lower() == "windows"):
    os.system(
        f"pyinstaller --name={project_name} --windowed --onefile --add-data=Icon.svg;. __main__.py")
    shutil.move(os.path.join("dist", "IPNS-Manager.exe"),
                os.path.join("dist", f"IPNS-Manager_{platform.system().lower()}_{platform.machine().lower()}.exe"))
else:
    os.system(
        f"pyinstaller --name='{project_name}' --windowed --onefile --add-data='Icon.svg:.' __main__.py")
    shutil.move(os.path.join("dist", project_name),
                os.path.join("dist", f"{project_name}_{platform.system().lower()}_{platform.machine().lower()}"))
