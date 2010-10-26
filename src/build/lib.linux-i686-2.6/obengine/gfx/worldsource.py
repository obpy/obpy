__author__="openblocks"
__date__ ="$Aug 9, 2010 10:43:40 PM$"

from obengine.element import ElementFactory
from obengine.cfg import cfgdir
from obengine.gfx import get_rootwin

import xml.etree.ElementTree as xmlparser
from os.path import exists

from pandac.PandaModules import PandaNode, NodePath, CompassEffect

class WorldSource(list):

    def __init__(self, source):
        """
        source is a derivative of WorldSource(yes, kinda confusing...)
        Do NOT create this class! Create one of its derivatives, instead.
        """

        self.source = source

    def handle_brick(self, child):

        rgb = []
        coords = []
        orientation = []
        size = []
        anchored = False

        coordstr = child.attrib['coords'].replace(' ','')
        rgbstr = child.attrib['rgb'].replace(' ','')
        orient_str = child.attrib['orientation'].replace(' ','')
        size_str = child.attrib['size'].replace(' ','')
        name = child.attrib['name']

        if child.attrib.has_key('anchored'):

            if child.attrib['anchored'] == 'yes':

                anchored = True

            else:

                anchored = False

        coords.append(float(coordstr.split(',')[0]))
        coords.append(float(coordstr.split(',')[1]))
        coords.append(float(coordstr.split(',')[2]))

        rgb.append(int(rgbstr.split(',')[0]))
        rgb.append(int(rgbstr.split(',')[1]))
        rgb.append(int(rgbstr.split(',')[2]))

        orientation.append(float(orient_str.split(',')[0]))
        orientation.append(float(orient_str.split(',')[1]))
        orientation.append(float(orient_str.split(',')[2]))

        size.append(int(size_str.split(',')[0]))
        size.append(int(size_str.split(',')[1]))
        size.append(int(size_str.split(',')[2]))

        element = ElementFactory().make('brick', name, coords, rgb, size, orientation, False, anchored)


        self.append(element)

    def handle_skybox(self, child):

        skybox = None

        if child.attrib.has_key('path'):

            if exists('data/' + child.attrib['path']):

                skybox = get_rootwin().loader.loadModel('./data/' + child.attrib['path'])

            elif exists(cfgdir + '/data/' + child.attrib['path']):

                skybox = get_rootwin().loader.loadModel(cfgdir + '/data/' + child.attrib['path'])

        else:
            
            skybox = get_rootwin().loader.loadModel(cfgdir + '/data/sky')

        skybox.reparentTo(get_rootwin().camera)
        skybox.setEffect(CompassEffect.make(get_rootwin().render))
        skybox.setScale(5000)
        skybox.setShaderOff()
        skybox.setLightOff()


    def parse(self):
        
        file = self.source.retrieve()

        tree = xmlparser.parse(file)
        rootnode = tree.getroot()

        supported_tags = { 'brick' : 'handle_brick', 'skybox' : 'handle_skybox' }


        for child in rootnode:

            if child.tag in supported_tags:

                getattr(self, supported_tags[child.tag])(child)

class FileWorldSource(WorldSource):
    """
    This class loads a world from a file. Supply this to an obengine.world.World's load_world method.
    """

    def __init__(self, path):
        """
        path is the file path of the world to load.
        """

        WorldSource.__init__(self, self) # Yes, very wierd...
        self.path = path

    def retrieve(self):

        return open(self.path,'r')