import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine
import obengine.cfg
import obengine.log
import obengine.async
import obengine.plugin
import obengine.gfx.math

def main():

    obengine.cfg.Config().load('obconf.cfg')
    obengine.log.Logger().autoconfig()

    obengine.init()

    obengine.plugin.require('core.physics')
    obengine.plugin.require('core.graphics')

    import obplugin.core.graphics

    scheduler = obengine.async.Scheduler()

    window = obplugin.core.graphics.Window('OpenBlox', scheduler)

    light = obplugin.core.graphics.Light(obplugin.core.graphics.Light.AMBIENT, 'ambient light', window, obengine.gfx.math.Color(25, 25, 25, 255), False)
    light2 = obplugin.core.graphics.Light(obplugin.core.graphics.Light.DIRECTIONAL, 'directional light', window, obengine.gfx.math.Color(250, 250, 250, 255), False)

    model = obplugin.core.graphics.Model('brick-new.egg', window)
    model2 = obplugin.core.graphics.Model('brick-new.egg', window)

    window.on_loaded += light.load
    window.on_loaded += light2.load
    window.on_loaded += model.load
    window.on_loaded += model2.load
    window.on_loaded += lambda: window.start_rendering()

    def show():

        model.position = 0, 10, -5
        model.color = 0, 100, 0, 0
        model.scale = 4, 4, 1

        model.showing = True

        light2.look_at(model)

    def show2():

        model2.position = 0, 30, -5
        model2.color = 100, 0, 100, 255
        model2.scale = 1, 1, 1

        model2.showing = True

    def change_color(task):

        if model.load_okay == False:
            return task.AGAIN

        if model.color.g < 255:
            model.color = model.color.r, model.color.g, model.color.b, model.color.a + 5

        else:
            return task.STOP

        return task.AGAIN

    def change_hpr(task):

        if model2.load_okay == False:
            return task.AGAIN

        if model2.rotation.h > 360:
            model2.rotation.h = model2.rotation.h % 360

        else:
            model2.rotation.h += 1

        if model2.rotation.p > 360:
            model2.rotation.p = model2.rotation.p % 360

        else:
            model2.rotation.p += 1

        if model2.rotation.r > 360:
            model2.rotation.r = model2.rotation.r % 360

        else:
            model2.rotation.r += 1

        return task.AGAIN

    model.on_loaded += show
    model2.on_loaded += show2

    window.load()

    scheduler.add(obengine.async.PeriodicTask(change_color, 0.1))
    scheduler.add(obengine.async.Task(change_hpr, 0.05))

    scheduler.loop()
