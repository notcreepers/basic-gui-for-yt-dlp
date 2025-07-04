# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['gui-mac.py'],
    pathex=['/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp'],
    binaries=[
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/resources/yt-dlp', 'resources'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/resources/ffmpeg', 'resources')
    ],
    datas=[
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/resources/yt-dlp-gui-icon.png', 'resources'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/.venv/lib/python3.9/site-packages/sv_ttk', 'sv_ttk'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/.venv/lib/python3.9/site-packages/certifi/cacert.pem', 'certifi'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/.venv/lib/python3.9/site-packages/PIL/_imaging.cpython-39-darwin.so', 'PIL'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/.venv/lib/python3.9/site-packages/PIL/_tkinter_finder.py', 'PIL._tkinter_finder'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/.venv/lib/python3.9/site-packages/PIL/Image.py', 'PIL.Image'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/.venv/lib/python3.9/site-packages/PIL/ImageTk.py', 'PIL.ImageTk'),
        ('/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/.venv/lib/python3.9/site-packages/PIL', 'Pillow'),
    ],
    hiddenimports=['sv_ttk', 'certifi', 'PIL._tkinter_finder', 'PIL.Image', 'PIL.ImageTk', 'PIL', 'Pillow'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['setuptools'],
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
    name='gui-mac',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='/Users/gianni/Documents/VSC/basic-gui-for-yt-dlp/resources/yt-dlp-gui-icon.icns',
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    bundle_identifier='com.gianni.ytdlpgui',
)
