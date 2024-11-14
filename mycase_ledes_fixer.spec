# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import tkinterdnd2

block_cipher = None

# Get tkdnd library path
tkdnd_path = os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tkdnd')

a = Analysis(
    ['mycase_ledes_fixer.py'],
    pathex=[],
    binaries=[],
    datas=[
        (tkdnd_path, 'tkinterdnd2/tkdnd'),  # Include tkdnd library files
    ],
    hiddenimports=['ttkbootstrap', 'tkinterdnd2', 'tkdnd'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyCase-Ledes-Fixer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico'
) 