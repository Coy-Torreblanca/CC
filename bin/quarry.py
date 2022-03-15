#!/usr/bin/env python3
from cc import turtle, import_file

nav = import_file("/lib/nav.py")


def quarry(length, width, height):

    for z in range(height):
        for x in range(width):
            for y in range(length - 1):

                if turtle.detect():
                    turtle.dig()

                if not nav.forward():
                    return False

            nav.turnRight()
            if not nav.forward():
                return False
            nav.turnRight()

        if turtle.detectDown():
            turtle.digDown()

        if not nav.down():
            return False
