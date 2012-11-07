==========================
OpenBlox GUI Theming Guide
==========================

.. versionadded:: 0.8

As of OpenBlox 0.8, you can create custom themes for your game's GUI. This guide documents the OpenBlox
theme format so you can make your own themes and mod existing ones (where their licenses permit such modding, of course).

Overview
===============

A bare-bones OpenBlox GUI theme looks like this::

	/theme-name
		theme.ini
		/widgets
			/default
				normal.png
				highlight.png
				clicked.png
				disabled.png
		/fonts
			font-regular.ttf
			font-italic.ttf
			font-bold.ttf
			font-bolditalic.ttf
				
This directory structure represents the smallest-possible OpenBlox theme.
Here's an in-depth explanation of this structure:

Each theme is recognized when a folder contains a file named `theme.ini`. This file contains the name, author, and
license of the theme it defines. For example, here's the `theme.ini` file for the default theme that ships with OpenBlox:

.. code-block:: ini

	[theme]

	name = Default OpenBlox GUI theme
	author = DangerOnTheRanger
	license = Creative Commons Attribution 3.0 Unported (http://creativecommons.org/licenses/by/3.0/) for widgets,
    		  SIL Open Font License 1.1 for fonts

Inside the theme's root folder is the `widgets` folder. This folder contains several sub-folders which in turn
contain the background images - which must be in `.png` format - OpenBlox will theme its widgets with.
There are different backgrounds for different widgets states; the required states (and thus images) for
the `default` widget - the bare minimum required to make a valid theme - are:

* `normal`
* `highlight`
* `clicked`
* `disabled`

Some widgets might have extra states; if a background is not available for a certain widget's state,
the most appropriate default background will be loaded instead.

Each theme also must supply at least one font that will be used to render text. The naming of the font
is unimportant, but the only supported font formats at the moment are `.ttf` and `.otf`. Most themes
should include at least four fonts: One for regular text, one for italic text, one for bold text,
and one for bold plus italic text.
