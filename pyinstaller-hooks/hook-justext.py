from PyInstaller.utils.hooks import collect_all

data = collect_all('justext')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]

