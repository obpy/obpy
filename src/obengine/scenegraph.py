"""
Copyright (C) 2011 The OpenBlox Project

This file is part of The OpenBlox Game Engine.

    The OpenBlox Game Engine is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The OpenBlox Game Engine is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__="openblocks"
__date__ ="$May 23, 2011 8:33:32 PM$"

if __name__ == '__main__':

    import sys
    sys.path.append('..')

import functools
import sqlite3

import obengine.event
import obengine.datatypes
import obengine.utils
import obengine.depman

obengine.depman.gendeps()

class SceneGraph(object):
    """
    A SQLite-based scene graph.
    """

    _schema = '''
    CREATE TABLE scene_nodes (
        name TEXT,
        id INT,
        parent INT,
        children TEXT,
        primary key (id)
    )
    '''

    _add_node_sql = '''
    INSERT INTO scene_nodes (
    name,
    id,
    parent,
    children
    ) VALUES
    (
    ?,
    ?,
    ?,
    ?
    )'''

    _get_node_id_sql = '''
    SELECT * FROM scene_nodes WHERE
    id = ?
    '''

    _get_node_name_sql = '''
    SELECT * FROM scene_nodes WHERE
    name = ?
    '''

    _remove_node_id_sql = '''
    DELETE FROM scene_nodes WHERE
    id = ?
    '''

    _remove_node_name_sql = '''
    DELETE FROM scene_nodes WHERE
    name = ?
    '''

    _NO_PARENT_ID = -1
    _NO_CHILDREN_MARKER = '(none)'
    _CHILDREN_ID_SEP = ','

    def __init__(self):

        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row
        self.db.execute(self._schema)

        self.nodes = obengine.datatypes.EventDict()

    def add_node(self, node, error_on_exist = True):
        """
        Adds `node` to the scene graph. All of `node`'s children are added, as well.
        If `node`'s ID exists in the scene graph already, and `error_on_exist` is
        True, then `NodeIdExistsException` is raised.
        """

        if node.id in self.nodes:

            if error_on_exist is True:
                raise NodeIdExistsException(node.id)

            else:
                return

        node_name = node.name
        node_id = node.id
        parent_id = self._NO_PARENT_ID

        if node.parent is not None:
            parent_id = node.parent.id

        node_children = []

        for child in node.children.itervalues():

            node_children.append(str(child.id))
            self.add_node(child, False)

        node_children = self._CHILDREN_ID_SEP.join(node_children)
        node_children = node_children or self._NO_CHILDREN_MARKER

        args = (node_name, node_id, parent_id, node_children)

        cursor = self.db.cursor()
        cursor.execute(self._add_node_sql, args)
        
        self.nodes[node_id] = node

        node.on_name_changed += functools.partial(self._update_node_name, node)
        node.children.on_item_added += functools.partial(self._update_node_children, node)
        node.children.on_item_removed += functools.partial(self._update_node_children, node)
        node.on_parent_changed += functools.partial(self._update_node_parent, node)

    def remove_node_by_id(self, id):
        """
        Removes a node (with ID `id`) from the scene graph.
        It also recursively removes all its children.

        If there is no node with ID `id` in the scene graph,
        then `NoSuchIdException` is raised.
        """

        node = self.get_node_by_id(id)
        children = node.children.keys()

        for child_id in children:
            self.remove_node_by_id(child_id)

        cursor = self.db.cursor()
        cursor.execute(self._remove_node_id_sql, (id,))

        if node.parent:
            node.parent.remove_child(node.id)

        del self.nodes[id]

    def remove_node_by_name(self, name):
        """
        Removes a node (with name `name`) from the scene graph.
        It also recursively removes all its children.

        If no node named `name` exists, then NoSuchNameException is raised.
        """

        node = self.get_node_by_name(name)

        for child_id in node.children:
            self.remove_node_by_id(child_id)

        cursor = self.db.cursor()
        cursor.execute(self._remove_node_name_sql, (name,))

        node.parent.remove_child(node.id)

        del self.nodes[node.id]

    def get_node_by_id(self, id):
        """
        Retrieves the node with ID `id` from the scene graph.
        If the ID isn't in the scene graph, `NoSuchIdException` is raised.
        """

        cursor = self.db.cursor()
        cursor.execute(self._get_node_id_sql, (id,))

        rows = cursor.fetchall()
        rowcount = len(rows)

        if rowcount == 0:
            raise NoSuchIdException(id)

        id = rows[0]['id']
        return self.nodes[id]

    def get_node_by_name(self, name):
        """
        Retrieves the node named `name` from the scene graph.
        If there is more than one node named `name` in the scene graph,
        `AmbiguousNameException` is raised.

        If no node named `name` exists, then NoSuchNameException is raised.
        """

        cursor = self.db.cursor()
        cursor.execute(self._get_node_name_sql, (name,))

        rows = cursor.fetchall()
        rowcount = len(rows)

        if rowcount == 0:
            raise NoSuchNameException(name)

        elif rowcount != 1:
            raise AmbiguousNameException(name)

        id = rows[0]['id']
        return self.nodes[id]

    def _update_node_name(self, node, name):

        sql = '''
        UPDATE scene_nodes
        SET name = ?
        WHERE id = ?
        '''

        cursor = self.db.cursor()
        cursor.execute(sql, (name, node.id))

    def _update_node_children(self, node, child, child_node):

        update_sql = '''
        UPDATE scene_nodes
        SET children = ?
        WHERE id = ?
        '''

        children_str = self._CHILDREN_ID_SEP.join(map(str, node.children))
        cursor = self.db.cursor()

        cursor.execute(update_sql, (children_str, node.id))

        if child_node not in self.nodes:
            self.add_node(child_node)

    def _update_node_parent(self, node, parent_node):

        update_sql = '''
        UPDATE scene_nodes
        SET parent = ?
        WHERE id = ?
        '''

        parent_id = self._NO_PARENT_ID

        if parent_node:
            parent_id = parent_node.id

        cursor = self.db.cursor()
        cursor.execute(update_sql, (parent_id, node.id))


class SceneNode(object):
    """
    Generic scene node. You'll probably want to subclass this class,
    instead of using it directly.
    """

    _next_avail_id = 0
    
    def __init__(self, name, parent = None):
        """
        Initializes this scene node.
        Arguments:
        * `name` - the name of this node
        * `parent` - the parent of this node. If it is `None` (the default), then no parent is used.
        """

        self._name = name
        self._id = SceneNode._next_avail_id
        self._parent = parent

        if self.parent:
            self.parent.children[self.id] = self

        self.children = obengine.datatypes.EventDict()

        self.on_name_changed = obengine.event.Event()
        self.on_parent_changed = obengine.event.Event()

        SceneNode._next_avail_id += 1

    def remove_child(self, id):
        """
        Removes child with ID `id` from this node's list of children.
        It also recursively removes all that child's children, as well.

        If the child with ID `id` doesn't exist, NoSuchIdException is raised.
        """

        try:

            child_node = self.children[id]
            child_node.remove_all_children()

            del self.children[id]

        except KeyError:
            raise NoSuchIdException(id)

    def remove_all_children(self):
        """
        Removes all this node's children, and recursively removes
        all their children, as well.
        """

        children = self.children.iteritems()

        for id, child_node in children:

            child_node.remove_all_children()
            self.remove_child(id)

    def get_child_by_id(self, id):
        """
        Returns the child (with ID `id`) from this node's list of children.
        If this node doesn't have a child with said ID,
        then NoSuchIdException is raised.
        """

        try:
            return self.children[id]

        except KeyError:
            raise NoSuchIdException(id)

    def get_child_by_name(self, name):
        """
        Returns the child named `name` from this node's list of children,
        If this node doesn't have a child named `name`, then
        NoSuchNameException is raised.

        Otherwise, if this node has *more than one* child named `name`,
        then AmbiguousNameException is raised.

        *WARNING:* This method can be slow if this node has a lot of children (> 10000).
        In that case, you're better off using `SceneNode.get_child_by_id` (which takes O(n) time),
        `SceneGraph.get_node_by_name` which is *much* faster, or `SceneGraph.get_node_by_id`.

        Example:

            >>> sg = SceneGraph()
            >>> n1 = SceneNode('Node 1')
            >>> n2 = SceneNode('Node 2')
            >>> sg.add_node(n1)
            >>> n2.parent = n1
            >>> print n1.get_child_by_name('Node 2').name
            Node 2
        """

        search_results = obengine.utils.search_dict(self.children, name, lambda n: n.name)

        if len(search_results) == 0:
            raise NoSuchNameException(name)

        elif len(search_results) > 1:
            raise AmbiguousNameException(name)

        return self.children[search_results[0]]

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):

        if self.parent is not None or (new_parent is None and self.parent is not None):

            if self.parent.children.has_key(self.id):
                self.parent.remove_child(self.id)

        self._parent = new_parent

        if self.parent:
            self.parent.children[self.id] = self

        self.on_parent_changed(new_parent)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):

        self._name = new_name
        self.on_name_changed(self.name)

    @property
    def id(self):
        return self._id


class SceneGraphException(Exception):
    """Base class for scene graph-related exceptions."""
    pass


class NoSuchIdException(Exception):
    """Raised when a requested ID doesn't exist."""
    pass


class NodeIdExistsException(SceneGraphException):
    """
    Raised when a node's ID already exists on the scene graph,
    and the `error_on_exists` argument given to SceneGraph.add_node is True.
    """
    pass


class NoSuchNameException(SceneGraphException):
    """Raised when a requested name doesn't exist."""
    pass


class AmbiguousNameException(SceneGraphException):
    """
    Raised when a requested name has multiple occurences, i.e,
    there are multiple nodes with the requested name.
    """
    pass

if __name__ == '__main__':

    import doctest
    doctest.testmod()