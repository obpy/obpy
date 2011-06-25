import sys
import os
import functools

sys.path.append(os.path.abspath(os.path.join(os.pardir, os.pardir)))

import obengine.world
import obengine.async
import obengine.worldloader
import obengine.element

def loaded_cb(world):

    print 'World loaded'
    print 'Elements:'
    print world.element.nodes

def main():

    obengine.cfg.Config().load(os.path.join(os.pardir, os.pardir, 'obconf.cfg'))

    obengine.init()

    e1 = obengine.element.Element('Element 1')
    e2 = obengine.element.Element('Element 2')

    world = obengine.world.World('Test world', 1)
    sched = obengine.async.Scheduler()
    source = [e1, e2]

    loader = obengine.worldloader.WorldLoader(world, source, sched)
    loader.on_world_loaded += functools.partial(loaded_cb, world)

    loader.load()
    sched.loop()

if __name__ == '__main__':
    main()
