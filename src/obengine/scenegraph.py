# OpenBlox scene graph library (obengine.scenegraph)
# ==================================================
#
# Provides basic scene graph functionality.
#
# Copyright (C) 2011 The OpenBlox Project
# License: GNU GPL v3
#
# See doc/build/html/scenegraph.html for the primary source of documentation
# for this module.

__author__ = "openblocks"
__date__  = "$May 23, 2011 8:33:32 PM$"

import functools
import sqlite3
import warnings

import obengine.event
import obengine.datatypes
import obengine.utils
import obengine.depman

obengine.depman.gendeps()

NO_PARENT_ID = -1
NO_CHILDREN_MARKER = '(none)'
CHILDREN_ID_SEP = ','


class SceneGraph(object):
    """
    .. versionadded:: 0.7
    
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

    def __init__(self, owner = None):

        self.owner = owner

        self.db = sqlite3.connect(':memory:')
        self.db.row_factory = sqlite3.Row
        self.db.execute(self._schema)

        self.nodes = obengine.datatypes.EventDict()
        self.node_handlers = {}

    def add_node(self, node, error_on_exist = True):
        """
        Adds *node* to the scene graph. All of *node*'s children are added, as well.

        :param node: The node to add to the scene graph
        :type node: `SceneNode`
        :param error_on_exist: If this is `True` (the default), then if a node with *node*'s NID
                               is already in the scene graph, then `NodeIdExistsException` is raised
        :type error_on_exist: `bool`
        :raises: `NodeIdExistsException` if *error_on_exist* is `True` (the default), and a node
                  with *node*'s NID is already on the scene graph
        :returns: `None`
        """

        if node.nid in self.nodes:

            if error_on_exist is True:
                raise NodeIdExistsException(node.nid)

            else:
                return

        node_name = node.name
        node_id = node.nid
        parent_id = NO_PARENT_ID

        if node.parent is not None:
            parent_id = node.parent.nid

        node_children = []

        for child in node.children.itervalues():

            node_children.append(str(child.nid))
            self.add_node(child, False)

        node_children = CHILDREN_ID_SEP.join(node_children)
        node_children = node_children or NO_CHILDREN_MARKER

        args = (node_name, node_id, parent_id, node_children)

        cursor = self.db.cursor()
        cursor.execute(self._add_node_sql, args)
        
        self.nodes[node_id] = node

        name_updater = functools.partial(self._update_node_name, node)
        children_updater = functools.partial(self._update_node_children, node)
        parent_updater = functools.partial(self._update_node_parent, node)

        node.on_name_changed += name_updater
        node.children.on_item_added += children_updater
        node.children.on_item_removed += children_updater
        node.on_parent_changed += parent_updater

        self.node_handlers[node_id] = (name_updater, children_updater, parent_updater)
        node.on_add(self)

    def remove_node_by_id(self, nid):
        """
        Removes a node (with NID *nid*) from the scene graph.
        It also recursively removes all its children.

        :param nid: The NID of the node to remove
        :type nid: `int`
        :raises: `NoSuchIdException` if the requested NID couldn't be found
        :returns: `None`
        """

        node = self.get_node_by_id(nid)
        children = node.children.keys()
        event_handlers = self.node_handlers[nid]

        node.on_name_changed -= event_handlers[0]
        node.children.on_item_added -= event_handlers[1]
        node.children.on_item_removed -= event_handlers[1]
        node.on_parent_changed -= event_handlers[2]

        for child_nid in children:
            self.remove_node_by_id(child_nid)

        cursor = self.db.cursor()
        cursor.execute(self._remove_node_id_sql, (nid,))

        if node.parent:
            node.parent.remove_child(node.nid)

        del self.nodes[nid]
        del self.node_handlers[nid]

        node.on_remove()

    def remove_node_by_name(self, name):
        """
        Removes a node (with name *name*) from the scene graph.
        It also recursively removes all its children.

        :param name: The name of the node to remove
        :type name: `str`
        :raises: `NoSuchNameException` if the requested name couldn't be found;
                 `AmbiguousNameException` if more than one node on the scene graph is named *name*.
        :returns: `None`
        """

        node = self.get_node_by_name(name)
        self.remove_node_by_id(node.nid)

    def find_node_by_name(self, name, starting_nid = NO_PARENT_ID, fail_on_ambiguous = False, exc_on_non_existent = True):
        """
        Example:
        
            >>> sg = SceneGraph()
            >>> n1 = SceneNode('Node 1')
            >>> n2 = SceneNode('Node 2')
            >>> sg.add_node(n1)
            >>> n2.parent = n1
            >>> print sg.find_node_by_name('Node 2').name
            Node 2
        """

        search_sql = '''
            SELECT * FROM scene_nodes WHERE
            parent = ? AND
            name = ?
            '''

        cursor = self.db.cursor()
        cursor.execute(search_sql, (starting_nid, name))

        rows = cursor.fetchall()
        rowcount = len(rows)

        if rowcount > 0:

            if fail_on_ambiguous is True:
                raise AmbiguousNameException(name)

            else:

                nid = rows[0]['id']
                return self.nodes[nid]

        else:

            get_children_sql = '''
            SELECT * FROM scene_nodes WHERE
            parent = ?
            '''
            
            cursor = self.db.cursor()
            cursor.execute(get_children_sql, (starting_nid,))

            rows = cursor.fetchall()
            rowcount = len(rows)

            if rowcount > 0:

                for row in rows:

                    nid =  row['id']
                    node = self.find_node_by_name(name, nid, fail_on_ambiguous, False)

                    if node:
                        return node

            if exc_on_non_existent is True:
                raise NoSuchNameException(name)

            else:
                return None

    def get_node_by_id(self, nid):
        """
        Retrieves the node with NID *nid* from the scene graph.

        :param nid: The NID of the node to retrieve
        :type nid: `int`
        :returns: `None`
        :raises: `NoSuchIdException` if the requested NID couldn't be found
        :returns: `None`
        """

        cursor = self.db.cursor()
        cursor.execute(self._get_node_id_sql, (nid,))

        rows = cursor.fetchall()
        rowcount = len(rows)

        if rowcount == 0:
            raise NoSuchIdException(nid)

        nid = rows[0]['id']
        return self.nodes[nid]

    def get_node_by_name(self, name):
        """
        Retrieves the node named *name* from the scene graph.

        :param name: The name of the node to retrieve
        :type name: `str`
        :returns: `SceneNode` if a node named *name* was found
        :raises: `NoSuchNameException` if the requested name couldn't be found; `AmbiguousNameException` if more than one node on the scene graph is named *name*
        :returns: `None`
        """

        cursor = self.db.cursor()
        cursor.execute(self._get_node_name_sql, (name,))

        rows = cursor.fetchall()
        rowcount = len(rows)

        if rowcount == 0:
            raise NoSuchNameException(name)

        elif rowcount != 1:
            raise AmbiguousNameException(name)

        nid = rows[0]['id']
        return self.nodes[nid]

    def _update_node_name(self, node, name):

        sql = '''
        UPDATE scene_nodes
        SET name = ?
        WHERE id = ?
        '''

        cursor = self.db.cursor()
        cursor.execute(sql, (name, node.nid))

    def _update_node_children(self, node, child, child_node):

        update_sql = '''
        UPDATE scene_nodes
        SET children = ?
        WHERE id = ?
        '''

        children_str = CHILDREN_ID_SEP.join(map(str, node.children))
        cursor = self.db.cursor()

        cursor.execute(update_sql, (children_str, node.nid))

        if child_node not in self.nodes:
            self.add_node(child_node)

    def _update_node_parent(self, node, parent_node):

        update_sql = '''
        UPDATE scene_nodes
        SET parent = ?
        WHERE id = ?
        '''

        parent_id = NO_PARENT_ID

        if parent_node:
            parent_id = parent_node.nid

        cursor = self.db.cursor()
        cursor.execute(update_sql, (parent_id, node.nid))

    def __getattr__(self, key):

        if key in self.__dict__:
            return self.__dict__[key]

        try:

            node = self.get_node_by_name(key)

            warnings.warn(
            '''Attribute-style node access has been deprecated for OpenBlox 0.7,
            and will be removed in OpenBlox 0.8
            ''',
            category = DeprecationWarning,
            stacklevel = 2)

            return node

        except (NoSuchNameException, AmbiguousNameException):
            raise AttributeError(key)


class SceneNode(object):
    """
    Generic scene node. You'll probably want to subclass this class,
    instead of using it directly.
    """

    _next_avail_id = 0
    
    def __init__(self, name, parent = None):
        """
        Initializes this scene node.
        :param name: The name of this node
        :type name: `str`
        :param parent: The parent of this node (optional)
        :type parent: `SceneNode`
        """

        self._name = name
        self._nid = SceneNode._next_avail_id
        self._parent = parent

        if self.parent:
            self.parent.children[self.nid] = self

        self.children = obengine.datatypes.EventDict()

        self.on_name_changed = obengine.event.Event()
        self.on_parent_changed = obengine.event.Event()
        self.on_add = obengine.event.Event()
        self.on_remove = obengine.event.Event()

        SceneNode._next_avail_id += 1

    def remove_child(self, nid):
        """
        Removes child with NID *nid* from this node's list of children.
        It also recursively removes all that child's children, as well.

        :param nid: The NID of the child to be removed
        :type nid: `int`
        :returns: `None`
        :raises: `NoSuchIdException` if no child nodes have the NID *nid*
        """

        try:

            child_node = self.children[nid]
            child_node.remove_all_children()

            del self.children[nid]

            child_node.on_remove()

        except KeyError:
            raise NoSuchIdException(nid)

    def remove_all_children(self):
        """
        Removes all this node's children, and recursively removes
        all their children, as well.
        """

        children = self.children.iteritems()

        for nid, child_node in children:

            child_node.remove_all_children()
            self.remove_child(nid)

    def find_child_by_name(self, name, fail_on_ambiguous = False, exc_on_non_existent = True):
        """
        Recursively searches this node's children for the first node named *name*.

        :param name: The name of the requested node
        :type name: `str`
        :param fail_on_ambiguous: Raise an exception if multiple nodes matching *name*
                                  are found under the same node?
        :type fail_on_ambiguous: `bool`
        :param exc_on_non_existent: Raise an exception if no nodes named *name* were found?
        :returns: `SceneNode` if a node named *name* was found; *None*
                              if no nodes matching *name* were found and *exc_on_non_existent* is *True*
        :raises: `NoSuchNameException` if no node named *name* is a sub-node of this node,
                 `AmbiguousNameException` if multiple nodes are named *name* under the same
                 parent

        Example:

            >>> sg = SceneGraph()
            >>> n1 = SceneNode('Node 1')
            >>> n2 = SceneNode('Node 2')
            >>> n3 = SceneNode('Node 3')
            >>> n3.parent = n2
            >>> n2.parent = n1
            >>> sg.add_node(n1)
            >>> print n1.find_child_by_name('Node 3').name
            Node 3
        """

        if fail_on_ambiguous is False:

            try:
                return self.children[obengine.utils.search_dict(self.children, name, lambda n: n.name)[0]]

            except IndexError:
                pass

        else:

            try:
                return self.get_child_by_name(name)

            except NoSuchNameException:
                pass

        for child in self.children.itervalues():

            sub_child = child.find_child_by_name(name, fail_on_ambiguous, False)

            if sub_child:
                return sub_child

        if error_on_non_existent is True:
            raise NoSuchNameException(name)

        else:
            return None

    def get_child_by_name(self, name):
        """
        Returns the child named *name* from this node's list of children,
        If this node doesn't have a child named *name*, then
        NoSuchNameException is raised.

        Otherwise, if this node has *more than one* child named *name*,
        then `AmbiguousNameException` is raised.

        .. note::

            This method can be slow if this node has a lot of children (> 10,000).

        :param name: The name of the node to search for
        :type name: `str`
        :returns: `SceneNode` if the node was found
        :raises: `NoSuchNameException` if no node named *name* is a child of this node,
                  or `AmbiguousNameException` if multiple children of this node are named *name*

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

        else:
            return self.children[search_results[0]]

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):

        if self.parent is not None or (new_parent is None and self.parent is not None):

            if self.parent.children.has_key(self.nid):
                self.parent.remove_child(self.nid)

        self._parent = new_parent

        if self.parent:
            self.parent.children[self.nid] = self

        self.on_parent_changed(new_parent)

    @property
    def name(self):
        """
        The name of this scene node.
        Example:

            >>> sg = SceneGraph()
            >>> n1 = SceneNode('Node 1')
            >>> sg.add_node(n1)
            >>> print sg.get_node_by_name('Node 1').name
            Node 1
            >>> n1.name = 'Node 1 - changed name'
            >>> print sg.get_node_by_name('Node 1 - changed name').name
            Node 1 - changed name
            >>> print sg.get_node_by_name('Node 1')
            Traceback (most recent call last):
                ...
            NoSuchNameException: Node 1
        """
        return self._name

    @name.setter
    def name(self, new_name):

        self._name = new_name
        self.on_name_changed(self.name)

    @property
    def nid(self):
        return self._nid


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