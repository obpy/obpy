#!/usr/bin/env python

import sys
import os
import atexit

from zipfile import ZipFile
from optparse import OptionParser

import obengine
import obengine.gfx.worldsource as worldsource
from obengine.cfg import cfgdir

def get_opt(option, option_list):
    
    try:
        
        return getattr(option_list, option)
    
    except:
        
        return None
    
def on_exit():
    
    global tmpdir
    
    for filename in os.listdir('./'):
        
        os.remove(filename)
        
    os.chdir('..')
    os.rmdir(tmpdir)
    
def run_world(win):
    
    global world_name
    
    print 'Running...'
    
    src = worldsource.FileWorldSource('world.xml')
    src.parse()
    
    world = obengine.World(1, world_name)
    world.load_world(src)

parser = OptionParser()
parser.add_option('-f', '--file', dest = 'worldfile', help = 'world to load(in a zip file)')

(options, args) = parser.parse_args()

if not get_opt('worldfile', options):
    
    parser.print_help()
    sys.exit(0)
    
else:
    
    if not get_opt('worldfile', options).endswith('.zip'):
        
        print get_opt('worldfile', options), 'is not a zip file!'
        sys.exit(1)
        
    
    try:
        
        global tmpdir
        global world_name
        
        tmpdir = os.tmpfile()
        tmpdir = tmpdir.name
        
        os.mkdir(tmpdir)
        os.chdir(tmpdir)
        
        name = get_opt('worldfile', options)
        name = name[:len(name) - 4]
        
        world_name = name
        
        worldfile = ZipFile('..' + os.sep + get_opt('worldfile', options))
        worldfile.extractall()
        
        atexit.register(on_exit)
        
        obengine.gfx.init(run_world)
        
    except:
        
        print 'Exception!'