#!/usr/bin/env python

# This script generates terrain and a BloxWorks project from
# a heightmap and texturemap. Requires PIL be installed to run.
# See <TODO: no Sphinx docs yet - add some> for the main source of documentation
# for this script

#
# Copyright (C) 2011 The OpenBlox Project
#
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "Sep 12, 2011 11:30:16 AM"


import sys
import os
import optparse

import Image

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import obengine.math
import obengine.utils
import obengine.async
import obengine.plugin
import obengine.vfs
from obengine.elementfactory import ElementFactory

sys.path.append(os.path.join(os.path.dirname(__file__), 'bloxworks'))
import bloxworks.project
import bloxworks.packager
import bloxworks.gui.camera


MAX_HEIGHT = 10
BRICK_COLOR = obengine.math.Color(50, 205, 50)


def make_window(scheduler):

    import obplugin.core.graphics

    window = obplugin.core.graphics.Window('OBGenTerrain', scheduler)
    window.on_loaded += window.start_rendering
    window.load()
    return window


def make_sandbox():

    import obplugin.core.physics

    sandbox = obplugin.core.physics.World()
    sandbox.load()
    sandbox.pause()

    return sandbox


def init_elementfactory(window, sandbox):

    ElementFactory().set_window(window)
    ElementFactory().set_sandbox(sandbox)


def save_project():

    project = obengine.vfs.open('/bloxworks-registry/project').read()
    outfile = os.path.join(
                           obengine.vfs.getsyspath('/bloxworks-games/' + project.world.name),
                           bloxworks.project.WORLD_XML_FILE)

    saver = bloxworks.project.ProjectSaverVisitor(outfile)
    saver.accept(project)


def terrain_task(task, image_width, image_pixels, colormap_pixels, last_pos, max_height):

    current_pixel = image_pixels.pop()
    pixel_color = colormap_pixels.pop()
    rgb_range = (0, 255)
    height_range = (1, max_height)

    average_color = sum(current_pixel[:-1]) / 3
    brick_height = round(obengine.utils.interp_range(rgb_range,
                                                     height_range,
                                                     average_color))

    brick_pos = obengine.math.Vector(last_pos.x,
                                     last_pos.y,
                                     brick_height / 2)

    if brick_pos.x % image_width == 0:

        brick_pos.y += 1
        brick_pos.x = image_width

    brick_size = obengine.math.Vector(1, 1, brick_height)


#    print 'make brick with position(%s) and height(%s)' % (
#                                                           brick_pos,
#                                                           brick_size)

    has_alpha = True

    try:
        pixel_color[3]

    except IndexError:
        has_alpha = False

    if has_alpha is False or pixel_color[3] != 0:

        brick_name = ','.join(map(str, (brick_pos, pixel_color, brick_size)))
        element_factory = ElementFactory()

        brick = element_factory.make('brick', brick_name, brick_pos, pixel_color, brick_size, anchored = True)
        world = obengine.vfs.open('/bloxworks-registry/project').read().world
        world.add_element(brick)

    brick_pos.x -= 1

    last_pos.x = brick_pos.x
    last_pos.y = brick_pos.y

    if len(image_pixels) != 0:
        return task.AGAIN

    else:
        save_project()


def genterrain(image, colormap, window, max_brick_height = None, name = None, author = None):

    name = name or 'Generated terrain'
    author = author or 'Unknown'
    max_brick_height = max_brick_height or MAX_HEIGHT

    bloxworks.project.create_new_project(window, name, author)

    image_pixels = list(image.getdata())
    image_width, image_height = image.size
    num_pixels = image_width * image_height

    colormap_pixels = list(colormap.getdata())

    brick_pos = obengine.math.Vector(-image_width, image_height / 2)
    rgb_range = (0, 255)
    height_range = (1, MAX_HEIGHT)

    window.scheduler.add(obengine.async.Task(terrain_task, args = [image_width,
                                                                        image_pixels,
                                                                        colormap_pixels,
                                                                        brick_pos,
                                                                        max_brick_height]))


def run(window):

    option_parser = optparse.OptionParser()

    option_parser.add_option('-n',
                             '--name',
                             dest = 'name',
                             help = 'Name for the generated terrain (used in BloxWorks)',
                             default = None)

    option_parser.add_option('-a',
                             '--author',
                             dest = 'author',
                             help = 'Author of the generated terrain (used in BloxWorks)',
                             default = None)

    option_parser.add_option('-m',
                             '--max-height',
                             dest = 'max_height',
                             help = 'Maximum height of the generated terrain',
                             default = None)

    options, args = option_parser.parse_args()

    terrain_name = options.name
    terrain_author = options.author
    max_brick_height = options.max_height

    try:
        heightmap = Image.open(args[0])
    except IndexError:

        option_parser.print_help()
        sys.exit(1)

    try:
        colormap = Image.open(args[1])
    except IndexError:
        colormap = Image.open(args[0])

    sandbox = make_sandbox()
    init_elementfactory(window, sandbox)

    camera_controller = bloxworks.gui.camera.CameraController(window)

    genterrain(heightmap, colormap, window, max_brick_height, terrain_name, terrain_author)


def main():

    obengine.init()

    obengine.plugin.require('core.graphics')
    obengine.plugin.require('core.physics')

    scheduler = obengine.async.Scheduler()
    window = make_window(scheduler)
    window.on_loaded += lambda: run(window)

    scheduler.loop()


if __name__ == '__main__':
    main()
