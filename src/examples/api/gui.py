import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine
import obengine.math
import obengine.gui

def main():

    mbv1 = obengine.gui.MockButtonView('Click me!')
    mbv2 = obengine.gui.MockButtonView('Click me too!')
    mbv3 = obengine.gui.MockButtonView('Click me, too!')

    bm1 = obengine.gui.Button('Click me!', obengine.math.Vector2D(0, 0))
    bm2 = obengine.gui.Button('Click me too!', obengine.math.Vector2D(0, 0))
    bm3 = obengine.gui.Button('Click me, too!', obengine.math.Vector2D(0, 0))

    bp1 = obengine.gui.ButtonPresenter(bm1, mbv1)
    bp2 = obengine.gui.ButtonPresenter(bm2, mbv2)
    bp3 = obengine.gui.ButtonPresenter(bm3, mbv3)

    vb = obengine.gui.Container(obengine.gui.HorizontalLayoutManager)
    vb.add(bp1)
    vb.add(bp2)
    vb.add(bp3)

    print 'bp1.position:', bp1.position
    print 'bp2.position:', bp2.position
    print 'bp3.position:', bp3.position

if __name__ == '__main__':
    main()
