=================================
OpenBlox's documentation standard
=================================

General
=======

* All the reference documentation is written in American English.
  However, translations to other languages are welcome.
* Always run a spell-checker over your modified/created document,
  *before* committing it to the OpenBlox Mercurial repository.
* Perfect/near-perfect grammar is *mandatory* for the OpenBlox documentation.
  On the other hand, if you are just starting out
  speaking/writing American English (or are inexperienced with it, for any reason),
  then you can commit your modified/created document as-is, but you should
  state your document needs a grammar check in either (preferably both):
   
   * Your commit message
   * On the OpenBlox issue tracker (http://tracker.openblox.tuxfamily.org) - create
     a new ticket with a low priority stating your document needs a grammar check

Formatting
==========

* All of OpenBlox's official documentation is written in
  reST [1]_, and thus all the normal reST
  formatting rules apply.
* Use UNIX newline endings when you edit/create documents - they're used by default
  on Linux and Mac OSX. if you're using Windows and are unsure about how to
  configure your editor to use UNIX newlines, just run the script
  ``build-helpers\convert_newlines.py`` (by double-clicking on it) after you
  make all your changes to make your edited document use UNIX newlines.
* Always try to keep your lines under 80 characters long; if they're
  longer than that, break them up on a word boundary - Sphinx (the program that
  converts the reST-written documents into flat text or HTML) will automatically
  turn adjoining text into paragraphs.
   
.. rubric:: Footnotes

.. [1] http://sphinx.pocoo.org/rest.html