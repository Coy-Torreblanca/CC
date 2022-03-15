#!/usr/bin/env python3

from cc import import_file
import json

dig = import_file("/lib/dig.py")

with open("/data/trees.txt") as f:
    trees = json.loads(f.read())

dig.vien(trees)
