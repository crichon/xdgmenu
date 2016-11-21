XdgMenu
=======

**A ncurses application menu**.
*The missing stone of my i3 setup.*

Description
-----------

A simple and lightweight alternative to Desktop Environment's application menu. To be used when you do not remember the name of this new pdf reader you just installed yesterday night...

Dependencies:

- **PyXdg**: python's freedesktop bindings, used in order to generate the menu.
- **Urwid**: a framework build on top of ncurses.

Keybindings (case insensitive):

- **j,k,l,m or arrow**: Navigate between menu entries.
- **c**: Cycle through submenu. 
- **e**: on an application entry, launch it without exiting.
- **b**: on a submenu to go back to the parent menu.

Installation
------------

Pip:

    pip install xdgmenu

setuptools:

    python setup.py install

Configuration
-------------

Since i am using i3, a quick how-to integrate it in nicely.
Add to your **.i3/config**:

    set $term <your terminall emulator>

    bindsym <keybinding> $term -e 'xgmenu' --title xdgmenu
    for window [title="xdgmenu"] floating enable


Roadmap
-------

- Implement entry description on 'd' keypress (a simple text widget displaying the programm help).
- Implement a search mode.
- Find how to correctly handle logging with urwid application.
- Separate the urwid logic from the application one.
- Package and upload to pypi.

Tests
----

No test yet but contribution are welcomed ;)

