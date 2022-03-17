#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")
inv = import_file("/lib/inventory.py")

# chest: "minecraft:chest"

# passing args is not working
args = [0, 0, 0]


def put_chest():
    if not inv.search("minecraft:chest"):
        return False

    nav.turn_left()
    nav.turn_left()

    if turtle.detect():
        turtle.dig()

    turtle.place()

    if inv.search("minecraft:chest"):
        nav.turn_left()
        if nav.forward():
            nav.turn_right()
            if turtle.detect():
                turtle.dig()
            turtle.place()
            nav.turn_left()
            nav.back()
        nav.turn_right()

    nav.turn_left()
    nav.turn_left()


def quarry(length, width, height):

    nav = nav.nav()
    if not inv.search("minecraft:chest"):
        return False

    turn = nav.turn_left

    z_levels_chest = int(length * width) / (64 * 16)

    for z in range(height):
        for x in range(width):
            for y in range(length - 1):

                if turtle.detect():
                    turtle.dig()

                if not nav.forward():
                    return False

            if x != width - 1:

                turn = nav.turn_right if turn == nav.turn_left else nav.turn_left

                turn()

                if turtle.detect():
                    turtle.dig()

                if not nav.forward():
                    return False

                turn()

        if z != height - 1:
            if turtle.detectDown():
                turtle.digDown()

            if not nav.down():
                return False

            turn()
            turn()


if len(args) < 3:
    print("usage: quarry <length> <width> <height>")
else:
    length, width, height = [int(x) for x in args[:3]]
    quarry(length, width, height)
