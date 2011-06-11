====================================================
OpenBlox scene graph library (`obengine.scenegraph`)
====================================================

:synopsis: Basic scene graph library.
:copyright: 2011 The OpenBlox Project
:license: GNU GPL v3

.. versionadded:: 0.7

Overview
========

``obengine.scenegraph`` provides a simple, SQLite [1]_-based scene graph implementation.
Before OpenBlox 0.7, the only "scene graph" available was `obengine.datatypes.AttrDict`, and that class
had several shortcomings:

* Scene nodes were *required* to use unique names - this was unacceptable for OpenBlox 0.7, with the release of BloxWorks (with which users would make large [> 2,000 element] worlds with many elements sharing the same name)
* If scene nodes had duplicate names, they overwrote each other, without any errors or warnings whatsoever
* There was no concept of parenting, or nested nodes

To address these issues, this module, `obengine.scenegraph`, was born.

Concepts
========

Each node on the scene graph has its own unique ID number (node ID/NID) - no two nodes (no matter when or where they were created)
have identical ID numbers. So, each node's primary means of identification is through its NID.
The benefits of using node IDs to access your nodes are:

* O(1) time when using a NID from an `obengine.scenegraph.SceneNode`
* Each NID will never change - you can refer a node by its NID for the duration of its existence
* Each NID is globally unique - you can access a node by calling `obengine.scenegraph.SceneGraph.get_node_by_id` *without* having to nest calls to `obengine.scenegraph.SceneNode.get_child_by_id`
* You can have several scene nodes with identical names, and you can still differentiate between them using their NID

There are 2 main weaknesses with NIDs:

* The main problem with NIDs is that since each NID is automatically generated, you must hold a reference to the owning scene node to retrieve its NID (or you can look up its NID in BloxWorks)
* They aren't very expressive - constants that stand for NIDs are about as good as it gets with respect to readability

Because of these shortcomings, each scene node also has a user-defined name, which can also be used to access a scene node.
The advantages of using scene node names are:

* They are *extremely* expressive and easy to remember
* You already know the node's name, since you defined it; this is related to the first advantage

However, node names also have some problems:

* Since it's a possibility that more than 1 node can have the same name (especially at the root level), node names cannot be used to access a node where there is more than 1 node with the same name
* Searching for nodes using names with `obengine.scenegraph.SceneNode.get_child_by_id` takes O(N) time

It is up to you to decide which identification method better suits your purposes. The best strategy right now looks like this:

* Use NIDs for nodes (especially bricks, scripts, and the like) that you'll never access from a Lua script
* Use a unique name for each node you want to access from a Lua script

Examples
========


Basic usage:

   >>> from obengine.scenegraph import *
   >>> sg = SceneGraph()
   >>> n1 = SceneNode('Node 1')
   >>> sg.add_node(n1)
   >>> print sg.get_node_by_name('Node 1').name
   Node 1

Nodes can have names, but they must be unique *within their scope*, i.e,
their parent can have no other children with the same name, if you want to be able to use `obengine.scenegraph.SceneNode.get_child_by_name`:

   >>> n2 = SceneNode('Node 2')
   >>> n3 = SceneNode('Node 2')
   >>> sg.add_node(n2)
   >>> n3.parent = n1
   >>> print n1.get_child_by_name('Node 2').name
   Node 2

But, if we try to use `obengine.scenegraph.SceneGraph.get_node_by_name`, what happens?

   >>> print sg.get_node_by_name('Node 2').name
   Traceback (most recent call last):
      ...
   AmbiguousNameException: Node 2

This occurred because the scene graph wasn't able to figure out which node with the name **Node 2** you wanted: **n1** or **n2**.

Module reference
============================

.. automodule:: obengine.scenegraph
   :members:

.. rubric:: Footnotes

.. [1] http://sqlite.org - the SQLite website
