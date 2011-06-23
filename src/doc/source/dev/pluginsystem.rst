========================
OpenBlox's plugin system
========================

Overview
========

OpenBlox has an powerful plugin system, that you can use to easily extend OpenBlox.
In fact, OpenBlox itself depends to a great degree on its plugin system, and comes with
plugins for:

* 3D/2D rendering
* Physics
* Audio
* Keyboard support
* GUI widgets

Plugins are written as normal Python modules or packages, so there's basically no
learning curve involved. The only new skill you *might* have to learn is the ``.ini`` file
syntax, but it's also very simple.

Tutorial
========

This tutorial will guide you through the process of making your very own OpenBlox plugin.

First, make a new directory inside your OpenBlox installation folder's ``plugins``
directory. It doesn't matter what it's called, but for the purposes of this
tutorial, we'll call it ``my-plugin``.

Next, add a file called ``plugin.ini`` (inside the ``my-plugin`` directory you just
created). Unlike the ``my-plugin`` directory, precise
naming (spelling, letter case, and file extension) is *crucial*, otherwise OpenBlox won't
recognize your plugin.

In your ``plugin.ini`` file, write this:

.. code-block:: ini

    [core]

    name = My first plugin
    module = my_plugin

    provides = virtual.plugin


Let's go over each of those variables:

* ``name`` - The name of your plugin. This can be anything you want, but it should be descriptive
* ``module`` - This specifies the Python module/package the OpenBlox plugin manager
    should import to expose your plugin to it's users. It will be imported (and exposed) just
    like a normal Python module/package, so if it doesn't implement any virtual
    plugins [1]_, make sure it's a valid Python name!
*  ``provides`` - This tells the OpenBlox plugin manager what virtual plugins [1]_
   your plugin provides. If your plugin provides more than one virtual plugin,
   they should be seperated by commas.

We have to actually write your plugin's code now. Type the following into a file
called ``my_plugin.py``, located inside the ``my-plugin`` directory you made earlier:

.. code-block:: python

    # This is a simple plugin. Note how it's indistinguishable from a
    # normal Python module.

    def init():
        """Initializes this plugin
        This method will get called when this plugin
        is loaded. Note that all plugins you write need not have this method.
        If it doesn't exist, it is not called.
        """
        print 'My plugin was just initialized!'

    def test_function():
        """A custom function
        This is a custom function that your users can call,
        just like a normal Python function.
        """
        return 'This was returned from a plugin!'

Now, start up your Python interpreter. Make sure the current working directory
is the directory you installed OpenBlox in (i.e, when you list the current working
directory's contents, there should be an ``obengine`` directory).

Next, type this code into your interpreter (ignore the comments and whitespace,
they're just there to help you understand what you're doing):

.. code-block:: python

    # Import OpenBlox, and OpenBlox's plugin code

    import obengine
    import obengine.plugin

    # This is a little tricky. Remember in
    # plugin.ini, when you added the "provides = virtual.plugin" line?
    # Well, this is when that line comes into play.
    # OpenBlox's plugin manager will scan its list of known plugins,
    # looking for a plugin that implements "virtual.plugin".
    # When it finds it, it loads and initalizes that plugin.

    obengine.plugin.require('virtual.plugin')

    # Now, we import your plugin, just like a normal Python module.
    # Note that the obplugin package is a virtual package provided by OpenBlox when
    # you import obengine.plugin; it doesn't really exist.
    # Note also that it correctly parses period-delimited names, so you can
    # use periods as a method of organization.

    import obplugin.virtual.plugin

    # Another note: you could've imported your plugin with this line, instead:
    # import obplugin.my_plugin

    print obplugin.virtual.plugin.test_function()

The output from the above script should be::

    My plugin was just initialized!
    This was returned from a plugin!

.. rubric:: Footnotes

.. [1] A *virtual plugin* is a plugin that doesn't explicitly exist, i.e, it
       is merely an agreed-upon interface, nothing more. An actual plugin can
       claim to *provide* a virtual plugin, and when that virtual plugin is
       required by some code, that actual plugin is loaded in its place.