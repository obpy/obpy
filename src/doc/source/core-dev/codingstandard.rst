============================
The OpenBlox coding standard
============================

This is the OpenBlox coding standard, which
closely follows Python PEP 8 (http://www.python.org/dev/peps/pep-0008/).
If you have any questions concerning this document, send
a message to OpenBlox (http://openblox.sf.net/users/openblox).

.. note::

    If you haven't already, read the :doc:`OpenBlox CLA (Contributor License Agreement) </core-dev/cla>`.

General
=======

* Indentation is done with 4 spaces. Never, *ever*, use tabs.
* Use UNIX-style newline endings for all files you create/modfiy.

.. note::

    The build-helper ``convert_newlines.py`` will automatically convert
    all your newlines for you. To run it on Windows (assuming you're in
    the ``build-helpers`` directory), type:

    .. code-block:: sh

        python convert_newlines.py
        # If Python isn't contained in one of the directories specified in your
        # %PATH% environment variable (which is the case when you install Python)
        # use this command, instead:
        # C:\Python26\python convert_newlines.py

    To run it on \*nix (i.e, Linux, Mac OSX, \*BSD) (again, assuming you're in the
    ``build-helpers`` directory):

    .. code-block:: sh

        ./convert_newlines.py
        # If the env program isn't installed inside /usr/bin on your system,
        # use this command instead:
        # python convert_newlines.py

Comments
========

* Regular comments (beginning with #) have a space after the hash, ``# like this``.
* If the comment is for a conditional construct, the comment is placed immediately proceeding the construct.
* If the comment is for an assignment or a regular line of code (method call, class creation, etc...), the comment is placed immediately proceeding the code.
* If the comment is a block comment (i.e, it spans several physical lines), then it should end with a period.

Examples::

    # Set a
    a = 1

    # complicated_method is complex,
    # so we need several lines to explain it, and we
    # end this explanation with a period.
    
    complicated_method(f, o, o, b, a, r, s, p, a, m, e, g, g, s)

Docstrings
==========

* Every module, function, and public class method should have a docstring.
* Docstrings should be written with normal text.

* A docstring's basic format is this::

    """Quick one-liner summary (no ending period)
    In-depth explanation of whatever this docstring belongs to.
    This includes explanation of parameters (and their expected type), return value,
    and possibly raised exceptions (where applicable).
    As you can see, each sentence has an ending period.
    """

* If the docstring belongs to a function, method, or class, then it should have 
  a small doctest suite (normally 2-4 complete tests [i.e, 2-4 tests of
  that docstring's owner] are fine), to provided regression testing,
  and to provide a form of runnable documentation.

Unit testing
============

A unit test is like the doctests inside a docstring (indeed, they look basically
identical), but each unit test is in a seperate file, contained in the ``test-suite``
directory.

* All classes and functions in OpenBlox are *required* to have unit tests.
* Each unit test's extension should be ``.txt``.
* You should mirror the directory structure of OpenBlox's code when
  you add a new unit test inside the ``test-suite`` directory. For example,
  if you're writing a unit test for `obengine.cfg.Config`, then you should name
  your unit test file ``test-suite/obengine/cfg.txt``.

Example::

    This is an example unit test comment. It is ignored by the test runner.
    The next two lines are run by the test runner, as they both start with
    ">>> ".
    >>> import obengine.cfg
    >>> cfg = obengine.cfg.Config()
    >>> cfg is cfg
    True

    See? Just like a normal doctest.
    This line is also ignored.

Variables
=========

* Variables are named ``like_this`` (Constants, however, are named ``LIKE_THIS``).
* Variables are declared at the start of their owning module or class.
* There are 2 blank lines between the last variable declaration, and the first coding construct, or method declaration(if the variable is global).

Examples::

    foo_bar = 0
    eggs_n_spam = [ 0, 1, 2, 3, 4, 5]


    #method declaration here

Coding Constructs
------------------

* All conditional and loop constructs are followed by a blank line, unless the following code is only one logical line.
* If the following logical line is a conditional or loop construct as well, the construct is *not* followed by a blank line.

Examples::

   # Single loop with single logical line
   for x in range(0, 5):
       print x

   # Single loop with multiple logical lines
   for x in range(1, 11):

      x += 5
      print x

   # Nested loops with single logical lines
   for x in range(0, 5):
      for y in range(0, 5):
         print 'Nested loops with one-loop instruction should look like this!'

   # Nested loops with multiple logical lines
   for x in range(0, 5):
      for y in range(0, 5):

         print 'This is inside a nested loop with multiple'
         print 'logical lines, so there is a blank line'
         print 'between the last loop declaration, and'
         print 'the first non-loop line'
         
Methods/Functions
=================

* Methods are named ``like_this``.
* Private methods begin with ``_``.
* Methods are fully documented, which means basic behavior, and each parameter is explained, as well as the expected type.
* Documentation is written as a multi-line string, began and terminated with ``"""``.
* There is a space after every parameter's terminating , character. This also applies to method calls.

Example::

    def do_x(a, b, c):
        """Does x
        Prints a, the first element of b, and the second element of c,
        all on a single line.
        """

        print a, b[0], c[1]


Classes
=======

* Classes are titled ``LikeThis``.
* If the class does not *need* to inherit from anything in partictular, it needs to inherit from object (to ensure compatability with Python 2.6/2.5).
* The first method defined is *always* ``__init__``.
* ``__init__`` must always be documented.
* Every method that is not private is given documentation.
* Private methods can have doocumentation, but it's not required. Private methods, *at the very least*, have a comment at their beginning explaining how they are supposed to be used.
* There is also a blank line between the last line of a method, and the def line of the next one.
* Every class also has documentation, itself. Documentation, like methods, is written as a multi-line string, began and terminated with `"""`.

Example::

    class ClassA(object):
        """
        ClassA is for XYZ.
        Volatile - ClassA's interface might change in the future!
        """

        def __init__(self):
            """Initalizes ClassA
            No arguments are given.
            """
            print 'Initalized an instance of ClassA!'

        def foo(self, a):
            """Prints a
            Arguments:
             * a - the object to print
            Returns: None
            """

            self._bar(a)

        def _bar(self, a):
            print a

Modules
=======

* Modules have this header, at their beginning::

    #
    # <module description>
    # See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
    # for this module.
    #
    #
    # Copyright (C) <inital year released>-<last modified year> The OpenBlox Project
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

.. note::

    If your module has only been included (so far) in 1 version of OpenBlox, you can
    use this copyright line, instead::

        # Copyright (C) <inital year released> The OpenBlox Project

    Also, if your module hasn't been modified in every year it's been included
    with OpenBlox, use this copyright line::

        # Copyright (C) <inital year released>, <modified years, seperated by a comma> The OpenBlox Project

    For example, if your module was released in 2009, and was modified in 2010 *and* 2011,
    you should use::

        # Copyright (C) 2009-2011 The OpenBlox Project

    On the other hand, if your module was released in 2008, and modified in 2009 and 2011,
    you should use::

        # Copyright (C) 2008, 2009, 2011 The OpenBlox Project

.. note::

    If you are writing a Python package, then source files located in your package
    (save for ``__init__.py``) need not have the Sphinx documentation link. This doesn't
    apply to the `obengine` package, however.

* Modules are named ``likethis``.
* There are 2 blank lines between the terminating ``#`` of the header, and the first variable declaration.

.. _reST: http://docutils.sf.net/rst.html
