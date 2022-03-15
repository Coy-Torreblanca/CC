#!/usr/bin/env python3

from cc import turtle, import_file

nav = import_file("/lib/nav.py").nav()


def vien(desired_items):
    for _ in range(4):
        item = turtle.inspect()

        if item and item["name"] in desired_items:
            turtle.dig()
            turtle.forward()
            direction = nav.direction
            vein(desired_items)
            nav.turn_to(direction)
            nav.back()

        nav.turn_left()

    item = turtle.inspectUp()
    if item and item["name"] in desired_items:
        turtle.digUp()
        turtle.up()
        direction = nav.direction
        vein(desired_items)
        nav.turn_to(direction)
        nav.down()

    item = turtle.inspectDown()
    if item and item["name"] in desired_items:
        turtle.digDown()
        turtle.down()
        direction = nav.direction
        vein(desired_items)
        nav.turn_to(direction)
        nav.up()
