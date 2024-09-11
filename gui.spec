# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui.py'],
    pathex=['path/to/repo'],
    binaries=[('path/to/yt-dlp.exe', 'resources'), ('path/to/ffmpeg.exe', 'resources')],
    datas=[('path/to/yt-dlp-gui-icon.ico', '.'), ('path/to/sv_ttk', 'sv_ttk'), ('path/to/pywinstyles', 'pywinstyles')],
    hiddenimports=['sv_ttk', 'pywinstyles'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
	icon='path/to/yt-dlp-gui-icon.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
