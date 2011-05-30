def pytest_configure(config):

   import sys
   import os
   sys.path.append(os.path.abspath(os.curdir))
