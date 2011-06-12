import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

from obengine.utils import *

if __name__ == '__main__':

    given_range = (10, 100)
    requested_range = (10, 25)

    for x in range(*given_range):
        print interp_range(given_range, requested_range, x)
