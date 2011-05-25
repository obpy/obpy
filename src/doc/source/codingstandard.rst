========================
OpenBlox Coding Standard
========================

Copyright (C) 2011 The OpenBlox Project

Overview
---------

This is the OpenBlox coding standard, which closely follows Python PEP 8 (http://www.python.org/dev/peps/pep-0008/).
However, there are a few differences:

 * Usage of blank lines is encouraged
 * Docstrings are *required* to use reST

If you have any questions concerning this document, send a message to OpenBlox (http://openblox.sf.net/users/openblox).

Indentation
-----------

Indentation is done with 4 spaces. Never, *ever*, use tabs.

Comments
---------

Regular comments(beginning with #) have a space after the hash, `# like this`.

If the comment is for a conditional construct, the comment is placed immediately proceeding the construct.
If the comment is for an assignment or a regular line of code(method call, class creation, etc...),
the comment is placed immediately proceeding the code.

Examples::

    # Set a
    a = 1

    # complicated_method is complex,
    # so we need several lines to explain it
    
    complicated_method(f, o, o, b, a, r, s, p, a, m, e, g, g, s)

Docstrings
-----------

Every module, function, and public class method should have a docstring.
Docstrings should be written using reST_.

A docstring's basic format is this::

    """Quick one-liner summary (no ending period)
    In-depth explanation of whatever this docstring belongs to.
    As you can see, each sentence has an ending period.
    Also, this docstring uses *reStructuredText* (http://docutils.sf.net/rst.html).
    
    """

Variables
----------

Variables are named like_this.
(Constants, however, are named LIKE_THIS.)
Variables are declared at the start of their owning module or class.
There is a blank line between the last variable declaration, and the first coding construct, or method declaration(if the variable is global).

Examples::

    foo_bar = 0
    eggs_n_spam = [ 0, 1, 2, 3, 4, 5]

    #method declaration here

Coding Constructs
------------------

All conditional and loop constructs are followed by a blank line, unless the following code is only one logical line.
If the following logical line is a conditional or loop construct as well, the construct is *not* followed by a blank line.

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
         
Docstrings
------------------

Methods
--------

Methods are named `like_this`.

Private methods begin with _.

Methods are fully documented, which means basic behavior, and each parameter is explained, as well as the expected type.
Documentation is written as a multi-line string, began and terminated with """.

There is a space after every parameter's terminating , character.
This also applies to method calls.

Example::

    def do_x(a, b, c):
        """Does x.
        Prints a, the first element of b, and the second element of c,
        all on a single line.
        """

        print a, b[0], c[1]


Classes
--------

Classes are titled `LikeThis`.
If the class does not *need* to inherit from anything in partictular,
it needs to inherit from object (to ensure compatability with Python 2.6/2.5).

The first method defined is __init__.
Every method that is not private is given documentation.
Private methods can have doocumentation, but it's not required.

There is also a blank line between the last line of a method, and the def line of the next one.

Every class also has documentation, itself.
Documentation, like methods, is written as a multi-line string, began and terminated with """.

Examples::

    class ClassA(object):
        """
        ClassA is for XYZ.
        Volatile - ClassA's interface might change in the future!
        """

        def __init__(self):

            object.__init__(self)

        def foo(self, a):
            """
            Prints a.
            """

            self._bar(a)

        def _bar(self, a):
            print a

Modules
--------

Modules have this header, at their beginning::

    """
    <package name>
    ~~~~~~~~~~~~~~~~

    <Brief description and usage>

    :copyright: (C) <year> The OpenBlox Project
    :license: GNU GPL v3
    """

Modules are named likethis.
There is a blank line between the terminating """ of the header, and the first variable declaration.

.. _reST: http://docutils.sf.net/rst.html
