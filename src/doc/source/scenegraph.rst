================
The Scene Graph
================

Overview
========

Concepts
--------

IDs, names, parent/child relationship, etc...

Basic usage:

   >>> from obengine.scenegraph import *
   >>> sg = SceneGraph()
   >>> n1 = SceneNode('Node 1')
   >>> sg.add_node(n1)
   >>> print sg.get_node_by_name('Node 1').name
   Node 1

Nodes can have names, but they must be unique *within their scope*, i.e, 
their parent can no other children with the same name, if you want to be able to use `SceneNode.get_child_by_name`:

   >>> n2 = SceneNode('Node 2')
   >>> n3 = SceneNode('Node 2')
   >>> sg.add_node(n2)
   >>> n3.parent = n1
   >>> print n1.get_child_by_name('Node 2').name
   Node 2

But, if we try to use `SceneGraph.get_node_by_name`, what happens?

   >>> print sg.get_node_by_name('Node 2').name
   Traceback (most recent call last):
      ...
   AmbiguousNameException: Node 2

General documentation
----------------------

 .. automodule:: obengine.scenegraph
   :members:
   
