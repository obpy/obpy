import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import panda3d.core

import obengine
import obengine.gui
import obengine.math
import obengine.async
import obengine.plugin


def draw_button(sched):

    import obplugin.core.gui

    def clicked():
        lv.text = 'Button Clicked!'

    container = obengine.gui.Container(obengine.gui.HorizontalLayoutManager)

    bv = obplugin.core.gui.ButtonView('Bigger Button!')
    container.add(bv)

    lv = obplugin.core.gui.LabelView('Label')
    container.add(lv)

    ev = obplugin.core.gui.EntryView('Initial text')
    container.add(ev)

    rv = obplugin.core.gui.RadioView('Radio')
    container.add(rv)
    
    cbv = obplugin.core.gui.CheckboxView('Checkbox')
    container.add(cbv)


def main():

    obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))
    obengine.init()
    obengine.plugin.require('core.graphics')
    obengine.plugin.require('core.gui')

    import obplugin.core.graphics

    scheduler = obengine.async.Scheduler()
    window = obplugin.core.graphics.Window('OpenBlox', scheduler)

    window.on_loaded += window.start_rendering
    window.on_loaded += lambda: draw_button(scheduler)

    window.load()
    scheduler.loop()


if __name__ == '__main__':
    main()