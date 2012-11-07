#!/usr/bin/env python

# A graphical tool to configure the local OpenBlox installation.
# See <TODO: no Sphinx docs yet - add some> for the main source of documentation
# for this script.

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import sys
import os

sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.abspath(os.pardir))

import obengine.cfg
import obengine.async
import obengine.plugin
import obengine.gui


class ConfigOption(object):

    def __init__(self, container, name, option, section, validator = str, max_len = 30):

        self._validator = validator
        self._config_parser = obengine.cfg.Config()

        self._name = name
        self._option = option
        self._section = section

        widget_factory = obengine.gui.WidgetFactory()
        self._label = widget_factory.make('label', name)
        self._entry = widget_factory.make('entry', self._config_parser.get_str(option, section))

        self._entry.on_submitted += self._attempt_validation

        container.add(self._entry)
        container.add(self._label)

    def _attempt_validation(self):

        value = self._entry.text

        try:
            self._validator(value)

        except ValueError:

            self._entry.text = 'Invalid input'
            return


        self._config_parser.add_var(self._option, value, self._section)


def save_options():

    config_parser = obengine.cfg.Config()
    config_parser.save()


def create_window(scheduler):

    obengine.plugin.require('core.graphics')
    import obplugin.core.graphics

    window = obplugin.core.graphics.Window('OBConfig', scheduler)
    window.on_loaded += window.start_rendering
    window.load()

    return window


def create_gui():

    widget_factory = obengine.gui.WidgetFactory()
    container = widget_factory.make('container',
                                    position = obengine.math.Vector2D(0, -20),
                                    layout_manager = obengine.gui.VerticalLayoutManager)

    save_button = widget_factory.make(
                                      'button',
                                      'Save configuration')
    save_button.on_click += save_options
    container.add(save_button)

#    def key_validator(key_str):
#        if len(key_str) != 1:
#            raise ValueError
#
#    y_key = ConfigOption(
#                         container,
#                         'Y key',
#                         'y_key',
#                         'core.hardware',
#                         key_validator)
#    x_key = ConfigOption(
#                         container,
#                         'X key',
#                         'x_key',
#                         'core.hardware',
#                         key_validator)
#    b_key = ConfigOption(
#                         container,
#                         'B key',
#                         'b_key',
#                         'core.hardware',
#                         key_validator)
#    a_key = ConfigOption(
#                         container,
#                         'A key',
#                         'a_key',
#                         'core.hardware',
#                         key_validator)

    def bool_validator(bool_str):
        if bool_str not in ('yes', 'no'):
            raise ValueError

    use_vsync = ConfigOption(
                             container,
                             'Use VSync? (yes, no)',
                             'use-vsync',
                             'core.gfx',
                             bool_validator)

    use_shadows = ConfigOption(
                               container,
                               'Use shadows? (yes, no)',
                               'use-shadows',
                               'core.gfx',
                               bool_validator)

    def shading_validator(shading_str):
        if shading_str not in ('normal', 'toon', 'toon-full'):
            raise ValueError

    shading_model = ConfigOption(
                                 container,
                                 'Shading model (normal, toon, toon-full)',
                                 'shading',
                                 'core.gfx',
                                 shading_validator
                                 )

    def resolution_validator(res_str):

        components = res_str.split('x')

        if len(components) != 2:
            raise ValueError

        map(int, components)

    resolution = ConfigOption(
                              container,
                              'Screen resolution',
                              'resolution',
                              'core.gfx',
                              resolution_validator
                              )

    show_frame_rate = ConfigOption(
                                   container,
                                   'Show frame rate (yes, no)',
                                   'show-frame-rate',
                                   'core.gfx',
                                   bool_validator
                                   )

    def view_mode_validator(view_str):
        if view_str not in ('third-person', 'isometric', 'fps'):
            raise ValueError

    view_mode = ConfigOption(
                             container,
                             'Camera mode (third-person, isometric, fps)',
                             'view-mode',
                             'core.gfx',
                             view_mode_validator)

    frame_rate = ConfigOption(
                              container,
                              'Frame rate',
                              'frame-rate',
                              'core.gfx',
                              int)

    warning_label = widget_factory.make(
                                        'label',
                                        'WARNING: Improper settings could crash your OpenBlox installation!')
    container.add(warning_label)


def main():

    obengine.cfg.Config().load(os.path.abspath(os.path.join(os.pardir, 'obconf.cfg')))
    obengine.init()

    scheduler = obengine.async.Scheduler()
    window = create_window(scheduler)
    window.on_loaded += create_gui

    scheduler.loop()


if __name__ == '__main__':
    main()
