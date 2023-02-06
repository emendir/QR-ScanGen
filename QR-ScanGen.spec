# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['__main__.py'],
             pathex=[],
             binaries=[('C:\\Users\\weden\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\pyzbar\\libiconv.dll', '.'), ('C:\\Users\\weden\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\pyzbar\\libzbar-64.dll', '.')],
             datas=[('Icon.svg', '.')],
             hiddenimports=['pywifi', 'pyzbar', 'qrcode'],
             hookspath=[],
             hooksconfig={},
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
          name='QR-ScanGen',
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
          entitlements_file=None )
