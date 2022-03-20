#!/usr/bin/env python3

from cc import turtle

move_to_inspect = {
    turtle.up: turtle.inspectUp,
    turtle.down: turtle.inspectDown,
    turtle.forward: turtle.inspect,
}

move_to_dig = {
    turtle.up: turtle.dig,
    turtle.down: turtle.digDown,
    turtle.forward: turtle.dig,
}


def get_data():
    return move_to_inspect, move_to_dig
