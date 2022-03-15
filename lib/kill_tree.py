#!/usr/bin/env python3

from cc import turtle, import_file

nav = import_file("/lib/nav.py")
nav = nav.nav()


def kill_tree():
    print(nav.direction)
