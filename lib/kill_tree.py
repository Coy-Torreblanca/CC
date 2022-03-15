#!/usr/bin/env python3

from cc import turtle, import_file

nav = import_file("/lib/nav.py")
nav = nav.nav()

tree_db = ["minecraft:oak_log", "minecraft:oak_leaves"]


def kill_tree():
    for _ in range(4):
        item = turtle.inspect()

        if item and item["name"] in tree_db:
            turtle.dig()
            turtle.forward()
            direction = nav.direction
            kill_tree()
            nav.turn_to(direction)
            nav.back()

        nav.turn_left()

    item = turtle.inspectUp()
    if item and item["name"] in tree_db:
        turtle.digUp()
        turtle.up()
        direction = nav.direction
        kill_tree()
        nav.turn_to(direction)
        nav.down()

    item = turtle.inspectDown()
    if item and item["name"] in tree_db:
        turtle.digDown()
        turtle.down()
        direction = nav.direction
        kill_tree()
        nav.turn_to(direction)
        nav.up()
