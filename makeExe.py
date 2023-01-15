# To make executable it will require requirements.txt + nuitka
import os
import pkg_resources
from platform import system

installed = {pkg.key for pkg in pkg_resources.working_set}

if not 'nuitka' in installed:
    raise ModuleNotFoundError('install nuitka to make executable')

filepath = 'main.py' 

flags = ''

onefile = True
standalone = True
noconsole = True # only for Windows
icon = 'src/assets/icon.ico'

if onefile:
    flags += ' --onefile'

if standalone:
    flags += ' --standalone'

if noconsole:
    if system() == 'Windows':
        flags += ' --windows-disable-console'
    else:
        print('Disabling console is only on Windows')

if icon != '':
    if icon.endswith('.ico'):
        if system() == 'Windows':
            flags += f' --windows-icon-from-ico={icon}'

        if system() == 'Linux':
            flags += f' --linux-icon=={icon}'
    else:
        print('only .ico icons are supported')

os.system(f'cmd /k "nuitka {filepath} {flags}"')