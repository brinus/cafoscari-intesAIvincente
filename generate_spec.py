import sys
import os
from pathlib import Path

APP_NAME = "CaFoscari IntesAI Vincente"
MAIN_SCRIPT = "main.py"
BUNDLE_ID = "it.unive.cafoscari.intesaivincente"
SPEC_FILENAME = "intesAIvincente.spec"

DATAS = [
    ('resources', 'resources'),
]

HIDDEN_IMPORTS = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'rc_images',
]

EXCLUDES = [
    'tkinter',
    'matplotlib',
    'numpy',
]

ICON_WINDOWS = 'resources/icons/icon.ico'
ICON_MACOS = 'resources/icons/icon.icns'
ICON_LINUX = None

BUILD_TYPE = 'onedir'

def get_icon_path():
    if sys.platform == 'darwin':
        return ICON_MACOS
    elif sys.platform == 'win32':
        return ICON_WINDOWS
    else:
        return ICON_LINUX

def format_list(items, indent=1):
    if not items:
        return "[]"
    
    indent_str = "    " * indent
    formatted = "[\n"
    for item in items:
        if isinstance(item, tuple):
            formatted += f"{indent_str}('{item[0]}', '{item[1]}'),\n"
        else:
            formatted += f"{indent_str}'{item}',\n"
    formatted += "    " * (indent - 1) + "]"
    return formatted

def generate_spec_content():
    icon_path = get_icon_path()
    icon_line = f"icon='{icon_path}'," if icon_path and os.path.exists(icon_path) else "icon=None,"
    
    spec_template = f"""# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

datas = {format_list(DATAS)}

hiddenimports = {format_list(HIDDEN_IMPORTS)}

excludes = {format_list(EXCLUDES)}

a = Analysis(
    ['{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_line}
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{APP_NAME}',
)
"""

    if sys.platform == 'darwin':
        bundle_icon = ICON_MACOS if ICON_MACOS and os.path.exists(ICON_MACOS) else None
        bundle_icon_line = f"icon='{bundle_icon}'," if bundle_icon else "icon=None,"
        
        bundle_target = 'coll' if BUILD_TYPE == 'onedir' else 'exe'
        
        spec_template += f"""
# Bundle macOS .app
app = BUNDLE(
    {bundle_target},
    name='{APP_NAME}.app',
    {bundle_icon_line}
    bundle_identifier='{BUNDLE_ID}',
)
"""

    return spec_template

def main():
    print(f"Generating file {SPEC_FILENAME}...")
    print(f"   Operating System: {sys.platform}")
    print(f"   Build Type: {BUILD_TYPE}")
    print(f"   Icon: {get_icon_path() or 'None'}")

    if not os.path.exists(MAIN_SCRIPT):
        print(f"Error: {MAIN_SCRIPT} not found!")
        sys.exit(1)
    
    spec_content = generate_spec_content()
    
    with open(SPEC_FILENAME, 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print(f"File {SPEC_FILENAME} generated successfully!")
    print(f"\nTo build: pyinstaller {SPEC_FILENAME}")

if __name__ == "__main__":
    main()
