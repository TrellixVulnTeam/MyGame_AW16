from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['tkinter', 'sqlite3', 'math', 'webbrowser', 'pickle'],
                 'excludes': [],
                 'include_files':['foe.db']}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, target_name = 'gms.exe', icon='logo.ico')
]

setup(name='foe_gms',
      version = '4.0',
      description = 'pfs a mettre sur les gms',
      options = {'build_exe': build_options},
      executables = executables)
