# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['gmc_core.py'],
             pathex=['/home/secretone/git_repos/index/gmc'],
             binaries=[],
             datas=[
               ("config.yaml", "."),
               ("public_config.yaml", ".")
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='gmc',
          icon='assets\icon.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
