#!/usr/bin/env python3

from cc import turtle, import_file, gps

fuel_cost = {"move": 1}

refuel = import_file("/lib/fuel/fuel.py").refuel


def call_move(move):

    try:
        move()

    except BaseException as error:
        if error == "Out of fuel":
            refuel.refuel()

        try:
            move()
        except:
            return false

    return true


def up():
    return call_move(turtle.up)


def down():
    return call_move(turtle.down)


def forward():
    return call_move(turtle.forward)


def back():
    return call_move(turtle.back)


def turn_left():
    return turtle.turnLeft()


def turn_right():
    return turtle.turnRight()


def locate():
    return gps.locate()
