#!/usr/bin/env python

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


__author__="openblocks"
__date__ ="$Jun 7, 2011 6:33:43 PM$"


import sys
import tempfile
import zipfile
import types
import pickle
import zlib
import base64

try:
    import cStringIO as StringIO

except ImportError:
    import StringIO

runtime_sources = '''
%s
'''

game_sources = '''
%s
'''

WORLD_FILE_LOC = 'world.xml'

class RuntimeImporter(object):

    def __init__(self, source):
        self.source = source

    def find_module(self, fullname, path = None):

        if fullname in self.sources:
            return self

        if fullname + '.__init__' in self.sources:
            return self

        return None

    def load_module(self, fullname):

        try:

            module_src = self.sources[fullname]
            is_pkg = False

        except KeyError:

            module_src = self.sources[fullname + '._init__']
            is_pkg = True

        co = compile(module_src, fullname, 'exec')
        module = sys.modules.setdefault(fullname, types.ModuleType(fullname))
        module.__file__ = '%s/%s' % (__file__, fullname)
        module.__loader__ = self

        if is_pkg:
            module.__path__ = [fullname]

        exec co in module.__dict__

    def get_source(self, name):

        try:
            src = self.sources.get[name]

        except KeyError:
            src = self.sources.get(name + '.__init__')

        return src


def load_runtime():

    decoded_sources = pickle.loads(zlib.decompress(base64.decodestring(runtime_sources)))
    meta_importer = RuntimeImporter(decoded_sources)

    sys.meta_path.append(meta_importer)


def load_game(env, source, load_cb):

    import obengine.worldloader

    loader = obengine.worldloader.WorldLoader(env.world, source, env.scheduler)
    loader.on_world_loaded += load_cb

    loader.load()


def start_player():
    print 'TODO: Implement player HUD!'


def parse_game():

    import obengine
    import obengine.gfx.worldsource
    import obengine.elementfactory
    import obengine.environ

    obengine.init()

    env = obengine.environ.Environment()
    factory = obengine.elementfactory.ElementFactory()

    factory.set_window(env.window)
    factory.set_sandbox(env.sandbox)

    env.window.on_loaded += env.sandbox.load
    env.window.load()

    while env.sandbox.loaded is False:
        env.scheduler.step()

    world_source = obengine.gfx.worldsource.FileWorldSource(WORLD_FILE_LOC)
    world_source.parse()

    return env, world_source


def extract_game(sources):

    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)

    zipfile.ZipFile(StringIO.StringIO(sources), 'r').extractall()


def main():

    if runtime_sources == '\n%s\n' or game_sources == '\n%s\n':

        print >> sys.stderr, '''
        This script cannot be run as-is. Use the OBFreeze tool
        to pack and freeze an OpenBlox game, instead of using this script directly.
        '''

        sys.exit(1)

    load_runtime()
    extract_game(game_sources)
    env, world_src = parse_game()
    load_game(env, world_src)
    env.scheduler.loop()

if __name__ == "__main__":
    main()