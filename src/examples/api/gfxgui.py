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

    button = factory.make('button', 'Button')
    shutter.add(button)

    label = factory.make('label', 'Label')
    shutter.add(label)

    entry = factory.make('entry', 'A text entry')
    shutter.add(entry)

    radio = factory.make('radio', 'Radio')
    shutter.add(radio)
    
    checkbox = factory.make('checkbox', 'Checkbox')
    shutter.add(checkbox)

    button2 = factory.make('button', 'Another Button')
    shutter.add(button2)

    help_label = factory.make(
    'label',
    '''Move your mouse below this text to try out OpenBlox's widgets.
    As you'll see, all of the widgets are hidden when you move your mouse away from them.
    This is because all the widgets are contained in a shutter - an invisible panel that hides its contents
    when the mouse isn't hovering over it.''',
    obengine.math.Vector2D(0, 30))

    pulldown = factory.make(
    'pulldown',
    'A pulldown',
    obengine.math.Vector2D(0, -20))

    pulldown_label = factory.make('label', 'A label inside a pulldown!')

    pulldown.add(pulldown_label)


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