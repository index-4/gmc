pyinstaller gmc_core.py --onefile -n gmc  

## linux
cp dist/gmc /usr/local/bin

## win
copy gmc.exe to a directory that is in your PATH:
- user level -> most likely %appdata%/local/microsoft/windowsapps
- system wide -> %systemroot% ( needs admin rights )
