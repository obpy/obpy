# -*- mode: python -*-

import sys
import os.path

import panda3d.core
import direct

sys.path.append(os.path.abspath(os.curdir))

import obengine


a = Analysis([os.path.join(HOMEPATH,'support', '_mountzlib.py'), os.path.join(HOMEPATH,'support', 'useUnicode.py'), os.path.join('tools', 'obplay.py')],
             pathex=[os.path.dirname(obengine.__file__), os.path.dirname(panda3d.core.__file__), os.path.abspath(os.path.join(os.path.dirname(direct.__file__)))
])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join(os.pardir, 'build', 'bin-temp', 'obplay'),
          debug=False,
          strip=False,
          upx=True,
          console=0 )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=os.path.join(os.pardir, 'build', 'bin', 'obplay'))
