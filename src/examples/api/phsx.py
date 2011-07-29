import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine
import obengine.async
import obengine.plugin
import obengine.gfx.math
import obengine.depman

def main():

    obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))

    obengine.init()

    obengine.plugin.require('core.physics')
    obengine.plugin.require('core.graphics')

    import obplugin.core.physics
    import obplugin.core.graphics

    scheduler = obengine.async.Scheduler()

    window = obplugin.core.graphics.Window('OpenBlox', scheduler)

    light = obplugin.core.graphics.Light(obplugin.core.graphics.Light.AMBIENT, 'ambient light', window, obengine.gfx.math.Color(25, 25, 25, 255), False)
    light2 = obplugin.core.graphics.Light(obplugin.core.graphics.Light.DIRECTIONAL, 'directional light', window, obengine.gfx.math.Color(250, 250, 250, 255), False)

    model = obplugin.core.graphics.Model('brick.egg', window)
    model2 = obplugin.core.graphics.Model('brick.egg', window)

    world = obplugin.core.physics.World()
    box = obplugin.core.physics.Box(model, world, model, scheduler, False)
    box2 = obplugin.core.physics.Box(model2, world, model, scheduler, True)

    window.on_loaded += light.load
    window.on_loaded += light2.load
    window.on_loaded += model.load
    window.on_loaded += model2.load
    window.on_loaded += lambda: window.start_rendering()
    window.on_loaded += world.load

    def on_collision(_, __):
        print 'Collision!'

    def add_collision_cb_box():
        box.on_collision += on_collision

    def show():

        model.position = 0, 30, -5
        model.color = 100, 0, 100, 255
        model.scale = 4, 4, 1

        model.showing = True

        light2.look_at(model)

        box.on_loaded += lambda: box.enable()
        box.load()

    def show2():

        model2.position = 0, 34, -15
        model2.color = 100, 0, 0, 255
        model2.scale = 4, 4, 4

        model2.showing = True

        box2.on_loaded += lambda: box2.enable()
        box2.on_loaded += add_collision_cb_box
        box2.load()

    def start_world():
        world.unpause()

    world.on_loaded += start_world

    model2.on_loaded += show2
    model.on_loaded += show

    window.load()
    scheduler.loop()

if __name__ == '__main__':
    main()