#!/bin/bash
# MyPkg Installer
echo "🚀 MyPkg kuruluyor..."
pkg update && pkg upgrade -y
pkg install python python-pip ruby curl git -y
curl -L "https://raw.githubusercontent.com/Kullanici/Repo/main/mypkg.py" -o $PREFIX/bin/mypkg
chmod +x $PREFIX/bin/mypkg
mypkg update
echo "✅ Kurulum tamam! 'mypkg search' yazarak başlayabilirsin."
