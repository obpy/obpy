#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
#
# This file is part of The OpenBlox Game Engine.
#
#     The OpenBlox Game Engine is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     The OpenBlox Game Engine is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "Jul 22, 2012 6:21:07 PM"


import panda3d.core
import panda3d.egg

import obplugin.panda_utils


class ProceduralModel(obplugin.panda_utils.PandaResource):

    def __init__(self, vertices, faces, uv_coords = [], colors = [], use_smooth_shading = True):

        obplugin.panda_utils.PandaResource.__init__(self)

        self._vertices = vertices
        self._faces = faces
        self._uv_coords = uv_coords
        self._colors = colors
        self._use_smooth_shading = use_smooth_shading

        self._egg_data = panda3d.egg.EggData()
        self._egg_group = panda3d.egg.EggGroup()
        self._egg_vertex_pool = panda3d.egg.EggVertexPool('vertex-pool')
        self._egg_group.addChild(self._egg_vertex_pool)
        self._egg_data.addChild(self._egg_group)

    def load(self):

        self._generate_model()
        self.panda_node = render.attachNewNode(panda3d.egg.loadEggData(self._egg_data))

        render.analyze()

        self.on_loaded()

    def _generate_model(self):

        for vertex_index, _ in enumerate(self._vertices):

            vertex = panda3d.egg.EggVertex()
            vertex.setPos(panda3d.core.Point3D(self._convert_vector_to_point3d(self._vertices[vertex_index])))

            try:
                vertex.setColor(self.convert_color(self._colors[vertex_index]))
            except IndexError:
                pass

            try:
                vertex.setUv(self._convert_vector2d_to_point2d(self._uv_coords[vertex_index]))
            except IndexError:
                pass

            self._egg_vertex_pool.createUniqueVertex(vertex)

        for vertex_list in self._faces:

            polygon = panda3d.egg.EggPolygon()
            self._egg_group.addChild(polygon)

            for vertex_index in vertex_list:
                polygon.addVertex(self._egg_vertex_pool.getVertex(vertex_index))

        if self._use_smooth_shading is True:
            self._egg_data.recomputeVertexNormals(45)

        else:
            self._egg_data.recomputePolygonNormals()

        self._egg_data.removeUnusedVertices(True)

    def _convert_vector_to_point3d(self, vector):
        return panda3d.core.Point3D(vector.x, vector.y, vector.z)

    def _convert_vector2d_to_point2d(self, vector):
        return panda3d.core.Point2D(vector.x, vector.y)
