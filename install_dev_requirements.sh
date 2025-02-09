sudo apt-get install libzbar-dev -y
sudo apt install flatpak-builder
sudo apt install flatpak flatpak-builder
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo

flatpak install flathub org.kde.Platform//6.8
flatpak install flathub org.kde.Sdk//6.8
flatpak install flathub com.riverbankcomputing.PyQt.BaseApp/x86_64/6.8

pip install pyinstaller
