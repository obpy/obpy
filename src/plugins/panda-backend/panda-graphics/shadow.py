"""
                    Shadow.py   
    by
        ___ ____ ____ ____ ____ ____ ____ _  _
         |  |__/ |___ |___ |___ |  | |__/ |\/|
         |  |  \ |___ |___ |    |__| |  \ |  |
                   
    Directions:
                                     
    #create ShadowSystem before you draw
    ShadowSystem()
    #to attach shadow to one or more objects and ligths 
    Shadow(object,light)
    # genereate a shadow node
    shnode = sh.generate()
    # reparent it to the render
    shnode.reparentTo(render)
"""


from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", """
framebuffer-stencil #t
stencil-bits 8
""")

from pandac.PandaModules import CardMaker, NodePath, Vec3, Vec4, Point3
from pandac.PandaModules import GeomVertexReader, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, GeomVertexFormat
from pandac.PandaModules import StencilAttrib, ColorWriteAttrib, DepthWriteAttrib
from pandac.PandaModules import CullFaceAttrib
from pandac.PandaModules import *

def ShadowSystem(shadowColor = Vec4(0, 0, 0, .3)):
    """ creates an overly screen wich is drawn last wich is our shadow"""
    screen = StencilAttrib.make(
         1,
         StencilAttrib.SCFNotEqual,
         StencilAttrib.SOKeep,
         StencilAttrib.SOKeep,
         StencilAttrib.SOKeep,
         0,
         0xFFFFFFFF,
         0xFFFFFFFF)
    cm = CardMaker("screener")
    cm.setFrame(-1, 1, -1, 1)
    node = render2d.attachNewNode(cm.generate())
    node.setAttrib(screen)
    node.setColor(shadowColor)
    node.setTransparency(True)
    node.setBin("unsorted", 0)


class Connectivity:
    """ connectivity class which will be useful for many algorithms """

    class Face:
        """ logic face """
        vertexes = []
        plane = None
        edges = []
        neighbours = []
        visible = True

    class Plane:
        """ plane equation """
        a = 0
        b = 0
        c = 0
        d = 0

    def __init__(self, object):
        """ creates connectivity per objects basis """
        self.object = object
        self.faces = []
        self.process()
        self.computeConnectivity()

    def computeConnectivityOnFaseList(self, faceList):
        """ computes conectivey """
        # for every face in the list see if there is an edge
        # that matches on another face, then they are neighbours
        for faceA in faceList:
            for e1, edge1 in enumerate(faceA.edges):
                if faceA.neighbours[e1] == None:
                    for faceB in faceList:
                        if faceB != faceA:
                            next = False
                            for e2, edge2 in enumerate(faceB.edges):
                                if edge1[0] == edge2[0] and edge1[1] == edge2[1]:
                                    faceA.neighbours[e1] = faceB
                                    faceB.neighbours[e2] = faceA
                                    next = True
                                    break
                                elif edge1[1] == edge2[0] and edge1[0] == edge2[1]:
                                    faceA.neighbours[e1] = faceB
                                    faceB.neighbours[e2] = faceA
                                    next = True
                                    break
                            if next: break

    def computeConnectivity(self):
        """ now and little more compiles one """
        i = 0
        mach = {}
        # puts every vertex into a mach tabe inside a
        # list with faces that share that vertex
        for face in self.faces:
            for vertex in face.vertexes:
                vd = int(vertex[0] * 1000), int(vertex[1] * 1000), int(vertex[2] * 1000)
                if vd in mach:
                    mach[vd].append(face)
                else:
                    mach[vd] = [face]
        # now look through the list and see if any face matches   
        for matches in mach.itervalues():
            if len(matches) > 1:
                self.computeConnectivityOnFaseList(matches)

    def process(self):
        self.faces = []
        geomNodeCollection = self.object.findAllMatches('**/+GeomNode')
        for nodePath in geomNodeCollection:
            geomNode = nodePath.node()
            self.processGeomNode(geomNode)


    def processGeomNode(self, geomNode):
        for i in range(geomNode.getNumGeoms()):
            geom = geomNode.getGeom(i)
            state = geomNode.getGeomState(i)
            self.processGeom(geom)

    def processGeom(self, geom):
        vdata = geom.getVertexData()
        for i in range(geom.getNumPrimitives()):
            prim = geom.getPrimitive(i)
            self.processPrimitive(prim, vdata)

    def processPrimitive(self, prim, vdata):
        vertex = GeomVertexReader(vdata, 'vertex')
        prim = prim.decompose()
        for p in range(prim.getNumPrimitives()):
            s = prim.getPrimitiveStart(p)
            e = prim.getPrimitiveEnd(p)
            vertexes = []
            for i in range(s, e):
                vi = prim.getVertex(i)
                vertex.setRow(vi)
                v = vertex.getData3f()
                vertexes.append(v)
            face = self.Face()
            face.vertexes = vertexes
            face.plane = self.Plane()
            face.plane.a = vertexes[0][1] * (vertexes[1][2] - vertexes[2][2]) + vertexes[1][1] * (vertexes[2][2] - vertexes[0][2]) + vertexes[2][1] * (vertexes[0][2] - vertexes[1][2]);
            face.plane.b = vertexes[0][2] * (vertexes[1][0] - vertexes[2][0]) + vertexes[1][2] * (vertexes[2][0] - vertexes[0][0]) + vertexes[2][2] * (vertexes[0][0] - vertexes[1][0]);
            face.plane.c = vertexes[0][0] * (vertexes[1][1] - vertexes[2][1]) + vertexes[1][0] * (vertexes[2][1] - vertexes[0][1]) + vertexes[2][0] * (vertexes[0][1] - vertexes[1][1]);
            face.plane.d = -(vertexes[0][0] * (vertexes[1][1] * vertexes[2][2] - vertexes[2][1] * vertexes[1][2]) +
                vertexes[1][0] * (vertexes[2][1] * vertexes[0][2] - vertexes[0][1] * vertexes[2][2]) +
                vertexes[2][0] * (vertexes[0][1] * vertexes[1][2] - vertexes[1][1] * vertexes[0][2]));
            face.edges = [(vertexes[0], vertexes[1]), (vertexes[1], vertexes[2]), (vertexes[2], vertexes[0])]
            face.neighbours = [None, None, None]
            self.faces.append(face)

class Shadow:
    """ main class of the shadow """

    frontSide = StencilAttrib.make(
                1,
                StencilAttrib.SCFAlways,
                StencilAttrib.SOKeep,
                StencilAttrib.SOKeep,
                StencilAttrib.SOIncrement,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF)

    backSide = StencilAttrib.make(
                1,
                StencilAttrib.SCFAlways,
                StencilAttrib.SOKeep,
                StencilAttrib.SOKeep,
                StencilAttrib.SODecrement,
                0xFFFFFFFF,
                0xFFFFFFFF,
                0xFFFFFFFF)

    def __init__(self, object, light, light_type = 'directional'):
        """ connect the object with the light """
        self.object = object
        self.light = light
        self.light_type = light_type
        self.con = Connectivity(object)
        self.faces = self.con.faces

    def lightFaces(self):
        """ runs through all the faces and see if they are lit """
        l = self.light.getPos(self.object)
        for face in self.faces:
            side = (face.plane.a * l[0] +
                face.plane.b * l[1] +
                face.plane.c * l[2] +
                face.plane.d)
            #print side
            if side > 0 :
                face.visible = True
            else:
                face.visible = False

    def generate(self):
        """ generate a shadow volume based on the light and the object """
        self.lightFaces()
        l = self.light.getPos(self.object)
        vdata = GeomVertexData('shadow', GeomVertexFormat.getV3() , Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        number = 0
        for face in  self.faces:
            if face.visible:
                for e, edge in enumerate(face.edges):
                    if face.neighbours[e] == None or not face.neighbours[e].visible:
                        v1 = edge[0]
                        v2 = v1 + (v1 - l) * 10
                        v3 = edge[1]
                        v4 = v3 + (v3 - l) * 10
                        vertex.addData3f(v1)
                        vertex.addData3f(v2)
                        vertex.addData3f(v3)
                        vertex.addData3f(v3)
                        vertex.addData3f(v2)
                        vertex.addData3f(v4)
                        number = number + 2
        prim = GeomTriangles(Geom.UHStatic)
        for n in range(number):
            prim.addVertices(n * 3, n * 3 + 1, n * 3 + 2)
        prim.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        geomnode = GeomNode('gnode')
        geomnode.addGeom(geom)
        try:
            self.front.removeNode()
            self.back.removeNode()
        except AttributeError:
            pass
        # make the 1st pass       
        self.front = NodePath("front")
        self.front.attachNewNode(geomnode)
        self.front.setColor(0, 0, 0, .1)
        self.front.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.MOff))
        self.front.setAttrib(CullFaceAttrib.makeReverse())
        self.front.setAttrib(DepthWriteAttrib.make(DepthWriteAttrib.MOff))
        self.front.setAttrib(self.frontSide)
        self.front.reparentTo(self.object)
        self.front.setBin("fixed", 1)
        # make the second pass
        self.back = NodePath("back")
        self.back.attachNewNode(geomnode)
        self.back.setColor(0, 0, 0, .1)
        self.back.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.MOff))
        self.back.setAttrib(CullFaceAttrib.make())
        self.back.setAttrib(DepthWriteAttrib.make(DepthWriteAttrib.MOff))
        self.back.setAttrib(self.backSide)
        self.back.reparentTo(self.object)
        self.back.setBin("fixed", 2)
        return NodePath("shadow of %s" % object)


if __name__ == "__main__":
    import direct.directbase.DirectStart
    # creae fore
    cm = CardMaker("back")
    cm.setFrame(10, -10, -10, 10)
    cmNode = render.attachNewNode(cm.generate())
    cmNode.setR(180)
    # load brick
    import os
    object = loader.loadModelCopy(os.path.abspath('../../../data/brick-flat'))
    object.reparentTo(render)
    object.setPos(4, 5, 4)
    object.setColor(0.7, 0.7, 0.7, 1)
    object.setScale(.7, .7, .7)
    object.setP(-90)
    base.cam.setPos(10, 10, -5)
    base.cam.lookAt(Point3(0, 0, 0), Vec3(0, 1, 0))
    # set up shadow system
    ShadowSystem()
    # create light
    light = NodePath("light")
    light.setPos(6, 6, 6)
    # attach shadow to object and light
    sh = Shadow(object, light)
    sh.generate()
    run()
