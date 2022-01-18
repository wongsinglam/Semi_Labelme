# -*- mode: python -*-
# vim: ft=python

import sys


sys.setrecursionlimit(5000)  # required on Windows


a = Analysis(
    ['semi_labelme/__main__.py'],
    pathex=['semi_labelme'],
    binaries=[],
    datas=[
        ('semi_labelme/config/default_config.yaml', 'semi_labelme/config'),
        ('semi_labelme/icons/*', 'semi_labelme/icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='semi_labelme',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    icon='semi_labelme/icons/icon.ico',
)
app = BUNDLE(
    exe,
    name='Semi_labelme.app',
    icon='semi_labelme/icons/icon.icns',
    bundle_identifier=None,
    info_plist={'NSHighResolutionCapable': 'True'},
)
