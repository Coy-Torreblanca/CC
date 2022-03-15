#!/usr/bin/env python3

from cc import import_file

dig = import_file("/lib/dig.py")
trees = import_file("/data/trees.py").get_data()

dig.vien(trees)
