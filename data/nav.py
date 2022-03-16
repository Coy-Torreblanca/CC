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
    ]
