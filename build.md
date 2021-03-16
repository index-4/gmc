## building
pyinstaller --clean gmc.spec  

## linux
cp dist/gmc /usr/local/bin

## win
copy gmc.exe to a directory that is in your PATH:
- user level -> most likely %appdata%/local/Microsoft/windowsapps
- system wide -> %systemroot% ( needs admin rights )