import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import panda3d.core

import obengine
import obengine.math
import obengine.async
import obengine.plugin


def draw_button(sched):

    obengine.plugin.require('core.gui')
    import obplugin.core.gui

    def clicked():

        print 'Before text change:', lv.size
        lv.text = 'Button Clicked!'
        print 'After text change:', lv.size
        print 'bv.size:', bv.size
        print 'ev.size:', ev.size

    bv = obplugin.core.gui.ButtonView('Button', obengine.math.Vector2D(30, 0), '../../data/sky1.png')
    bv.on_click += clicked

    lv = obplugin.core.gui.LabelView('Label')
    ev = obplugin.core.gui.EntryView(position = obengine.math.Vector2D(-70, 0))


def main():

    obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))
    obengine.init()
    obengine.plugin.require('core.graphics')

    import obplugin.core.graphics

    scheduler = obengine.async.Scheduler()
    window = obplugin.core.graphics.Window('OpenBlox', scheduler)

    window.on_loaded += window.start_rendering
    window.on_loaded += lambda: draw_button(scheduler)

    window.load()
    scheduler.loop()

if __name__ == '__main__':
    main()