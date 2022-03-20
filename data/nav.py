#!/usr/bin/env python3


def get_data():
    return [
        {
            "north": {"left": "west", "right": "east"},
            "west": {"left": "south", "right": "north"},
            "south": {"left": "east", "right": "west"},
            "east": {"left": "north", "right": "south"},
        },
        {"move": 1},
        {0: {1: "east", -1: "west"}, 1: {-1: "south", 1: "north"}},
        {
            "east": {"axis": 0, "direction": 1},
            "west": {"axis": 0, "direction": -1},
            "north": {"axis": 1, "direction": 1},
            "south": {"axis": 1, "direction": -1},
        },
    ]
