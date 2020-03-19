from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
files = [
    'icon.ico',
    "credentials.json"
]

buildOptions = dict(packages=[], includes=[], excludes=[], include_files=files)
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, targetName='QCReports')
]

setup(
    name='QcReportApp',
    version='1.2',
    description='QC Report helper application',
    options=dict(build_exe=buildOptions),
    executables=executables
)
