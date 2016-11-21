#!/usr/bin/python
# coding: utf-8

help = '''
Pymenu.py
---------

A simple ncurses base menu.
Use xdg specification in order to retrieve the installed application
and sort them in categories.
'''

import os
import logging
import subprocess
from pprint import pprint

import urwid
from xdg.Menu import parse, Menu, MenuEntry

log = logging.getLogger(__name__)
hdlr = logging.FileHandler('/tmp/dbug.log')
log.addHandler(hdlr)
log.setLevel(logging.DEBUG)

class MainFrame(urwid.Padding):

    def __init__(self):
        self.current_node = parse()
        self.stack = []
        menu = self.get_menu()
        super(MainFrame, self).__init__(menu, left=2, right=2)

    def update(self):
        '''Update the current frame based on the current node'''
        menu = self.get_menu()
        self.original_widget = menu
        if len(self.current_node.Entries) > 0:
            self.original_widget.focus_position = 2

    def get_menu(self):
        '''Generate a new menu based on the current node'''
        node = self.current_node
        title = node.Name
        choices = node.Entries
        menu = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            if isinstance(c, Menu):
                button = urwid.Button(c.Name)
            elif isinstance(c, MenuEntry):
                button = urwid.Button(c.DesktopEntry.getName())
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            menu.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(menu))

    def item_chosen(self, button, choice):
        '''Handle button event'''
        if isinstance(choice, Menu):
            self.stack.append((self.current_node, self.original_widget))
            self.current_node = choice
            self.update()
        elif isinstance(choice, MenuEntry):
            launch(choice)
            raise urwid.ExitMainLoop()

    def get_entry_in_focus(self):
        '''Return the DesktopEntry corresponding to the item in focus'''
        return self.current_node.Entries[self.original_widget.focus_position - 2]

    def cycle_submenu(self, reverse=False):
        '''Shortcut for cycling thgrough submenu of the same depth

        If launched from the root menu, step in the given category
        For the moment, this work on the assumption there is no
        MenuEntry and Menu in the same submenu
        '''
        step = 1
        if reverse: step = -1

        # if root node
        if self.current_node == parse():
            if not self.stack:
                self.stack.append((self.current_node, self.original_widget))
            focus = self.original_widget.focus_position - 2
            self.current_node = self.current_node.Entries[focus]
        else:
            node, widget = self.stack[-1]
            focus = widget.focus_position
            if focus <= 0:
                focus = len(node.Entries)
                widget.focus_position = focus
            if focus > len(node.Entries):
                focus = 1
                widget.focus_position = focus
            self.current_node = node.Entries[focus - 2 + step]
            widget.focus_position += step
        self.update()

    def keypress(self, seize, key):
        '''Custom keybindings'''
        super(MainFrame, self).keypress(seize, key)

        if key in ('b', 'B', 'h', 'H', 'left'):
            # recorver the parent menu and display it
            try:
                self.current_node, menu = self.stack.pop()
                self.original_widget = menu
            except IndexError:
                # do nothing if menu is the root menu
                pass
        # expand basic keybindings
        elif key in ('j', 'J'):
            super(MainFrame, self).keypress(seize, 'down')
        elif key in ('k', 'K'):
            super(MainFrame, self).keypress(seize, 'up')
        elif key in ('l', 'L', 'right'):
            super(MainFrame, self).keypress(seize, 'enter')
        elif key in ('c', 'C'):
            self.cycle_submenu(key=='C')

        # MenuEntry keybindings
        if len(self.current_node.Entries) > 0:
            choice = self.get_entry_in_focus()
            if isinstance(choice, MenuEntry):
                if key in ('d', 'D'):
                    pass
                if key in ('e', 'E'):
                    launch(choice)
        return key


def launch(choice):
    '''Use subprocess to launch an DesktopEntry using exo-open'''
    log.info('launching %s' % choice)
    with open(os.devnull) as null:
        # cmd = ['(', 'setsid', 'exo-open', ''.join([choice.getDir(), choice.Filename]), ')'],
        # cmd = ''.join(cmd)
        cmd = '(setsid exo-open ' + ''.join([choice.getDir(), choice.Filename]) + ')'
        log.info(cmd)
        rcode = subprocess.call(cmd,
            stdin=null, stdout=null, stderr=null, shell=True
        )
        if rcode != 0:
            log.error('error launching %s, return code %i' % (choice, rcode))

def exit_on_q(key):
    '''Handler for unhandled input'''
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def main():
    urwid.MainLoop(
        MainFrame(),
        palette=[('reversed', 'standout', '')],
        unhandled_input=exit_on_q
    ).run()

if __name__ == '__main__':
    main()

