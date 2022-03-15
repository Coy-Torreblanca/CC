#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")

# passing args is not working
args = [0, 0, 0]


def quarry(length, width, height):

    for z in range(height):
        for x in range(width):
            for y in range(length - 1):

                if turtle.detect():
                    turtle.dig()

                if not nav.forward():
                    return False

            nav.turn_right()
            if not nav.forward():
                return False
            nav.turn_right()

        if turtle.detectDown():
            turtle.digDown()

        if not nav.down():
            return False


if len(args) < 3:
    print("usage: quarry <length> <width> <height>")
else:
    length, width, height = [int(x) for x in args[:3]]
    quarry(length, width, height)
