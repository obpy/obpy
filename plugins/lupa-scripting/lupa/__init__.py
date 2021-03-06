# We need to enable global symbol visibility for lupa in order to
# support binary module loading in Lua.  If we can enable it here, we
# do it temporarily.

import sys

# Panda3D hack for errant Windows sys.path
if sys.platform == 'win32':
    sys.path.insert(0, 'C:\\Program Files\\OpenBlox\\obengine\\scripting')

def _try_import_with_global_library_symbols():
    import DLFCN
    import sys
    old_flags = sys.getdlopenflags()
    try:
        sys.setdlopenflags(DLFCN.RTLD_NOW | DLFCN.RTLD_GLOBAL)
        import lupa._lupa
    finally:
        sys.setdlopenflags(old_flags)

try:
    _try_import_with_global_library_symbols()
except:
    pass

del _try_import_with_global_library_symbols

# the following is all that should stay in the namespace:

from _lupa import *