#!/usr/bin/env python3

from cc import turtle, import_file, gps

# globals
fuel_cost = {"move": 1}
refuel = import_file("/lib/fuel/fuel.py").refuel
direction = "north"
direction_map = {
    "north": {"right": "west", "left": "east"},
    "west": {"right": "south", "left": "north"},
    "south": {"right": "east", "left": "west"},
    "east": {"right": "north", "left": "south"},
}


def call_move(move):

    try:
        move()

    except BaseException as error:
        if error == "Out of fuel":
            refuel.refuel()

        try:
            if not move():
                return False
        except:
            return False

    return True


def up():
    return call_move(turtle.up)


def down():
    return call_move(turtle.down)


def forward():
    return call_move(turtle.forward)


def back():
    return call_move(turtle.back)


def turn_left():
    direction = direction_map[direction]["left"]
    return turtle.turnLeft()


def turn_right():
    direction = direction_map[direction]["right"]
    return turtle.turnRight()


def turn_to(to_direction):
    while direction != to_direction:
        turn_right()


def locate():
    return gps.locate()
