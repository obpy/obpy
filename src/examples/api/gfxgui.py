import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))


import obengine
import obengine.gui
import obengine.math
import obengine.async
import obengine.plugin


def draw_button(sched):

    import obplugin.core.gui

    def clicked():
        lv.text = 'Button Clicked!'

    factory = obengine.gui.WidgetFactory()
    shutter = factory.make('shutter', position = obengine.math.Vector2D(0, 0))

    bv = obplugin.core.gui.ButtonView('Bigger Button')
    shutter.add(bv)

    lv = obplugin.core.gui.LabelView('Label')
    shutter.add(lv)

    ev = obplugin.core.gui.EntryView('A text entry')
    shutter.add(ev)

    rv = obplugin.core.gui.RadioView('Radio')
    shutter.add(rv)
    
    cbv = obplugin.core.gui.CheckboxView('Checkbox')
    shutter.add(cbv)

    bv2 = obplugin.core.gui.ButtonView('Button')
    shutter.add(bv2)


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