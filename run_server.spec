# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['run_server.py'],
             pathex=['/mnt/4ad1c2cb-209a-4390-886f-5a3b5cdf8a0a/mike/jectpro/school/northwestern/spring2020/cs338/WMW'],
             binaries=[],
             datas=[('search/middata/', 'search/middata/'), ('search/stopwords.txt', 'search/')],
             hiddenimports=['srsly.msgpack.util'],
             hookspath=['pyinstaller-hooks'],
             runtime_hooks=[],
             excludes=['torch'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='run_server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
