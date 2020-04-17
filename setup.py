from cx_Freeze import setup, Executable
import sys
import config

# Dependencies are automatically detected, but it might need
# fine tuning.
files = [
    'icon.ico',
    "credentials.json"
]

shortcut_table = [
    ("DesktopShortcut",  # Shortcut
     "DesktopFolder",  # Directory_
     config.NAME,  # Name
     "TARGETDIR",  # Component_
     f"[TARGETDIR]{config.NAME}.exe",  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     "",  # Icon
     0,  # IconIndex
     None,  # ShowCmd
     'TARGETDIR'  # WkDir
     )
]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {
    'data': msi_data,
    'initial_target_dir': f'[ProgramFilesFolder]\\{config.NAME}',
    'all_users': True,
    'install_icon': config.ICON_PATH,
    'upgrade_code': '{96e1b49d-40e8-4edc-8547-ceb4a9c0a619}',
}

buildOptions = dict(packages=[], includes=[], excludes=[], include_files=files)
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'main.py',
        base=base,
        targetName=config.NAME,
        icon=config.ICON_PATH
    )
]

setup(
    name=config.NAME,
    version=config.VERSION,
    description=config.DESCRIPTION,
    author="Ihor Magur",
    author_email="ihor.magur@devabit.com",
    options=dict(
        build_exe=buildOptions,
        bdist_msi=bdist_msi_options
    ),
    executables=executables
)
