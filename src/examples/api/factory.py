import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine.world
import obengine.async
import obengine.plugin
import obengine.elementfactory
from obengine.math import Color, EulerAngle

def main():

    obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))

    obengine.init()

    obengine.plugin.require('core.physics')
    obengine.plugin.require('core.graphics')

    import obplugin.core.graphics
    import obplugin.core.physics

    sched = obengine.async.Scheduler()
    window = obplugin.core.graphics.Window('OpenBlox', sched)
    sandbox = obplugin.core.physics.World()
    world = obengine.world.World('Test world', 1)

    factory = obengine.elementfactory.ElementFactory()
    factory.set_window(window)
    factory.set_sandbox(sandbox)

    def load_brick():

        light = obplugin.core.graphics.Light(obplugin.core.graphics.Light.AMBIENT, 'ambient light', window, obengine.math.Color(25, 25, 25, 255), False)
        light2 = obplugin.core.graphics.Light(obplugin.core.graphics.Light.DIRECTIONAL, 'directional light', window, obengine.math.Color(250, 250, 250, 255), False)

        light.load()
        light2.load()

        brick = factory.make('brick', 'Test brick', color = Color(25, 25, 42), rotation = EulerAngle(45, 45, 0))
        world.add_element(brick)
        brick.view.showing = True
        light2.look_at(brick.view.model)

    window.on_loaded += lambda: window.start_rendering()
    window.on_loaded += lambda: sandbox.load()
    sandbox.on_loaded += lambda: sandbox.unpause()
    sandbox.on_loaded += load_brick

    window.load()

    sched.loop()

if __name__ == '__main__':
    main()
