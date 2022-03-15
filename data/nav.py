#!/usr/bin/env python3


def get_data():
    return [
        {
            "north": {"right": "west", "left": "east"},
            "west": {"right": "south", "left": "north"},
            "south": {"right": "east", "left": "west"},
            "east": {"right": "north", "left": "south"},
        },
        {"move": 1},
    ]
